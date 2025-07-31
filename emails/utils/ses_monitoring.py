"""
AWS SES Monitoring and Analytics Utilities
Provides functions to monitor SES performance, quotas, and delivery statistics
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

import boto3
from botocore.exceptions import ClientError, BotoCoreError
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)


class SESMonitor:
    """
    AWS SES monitoring and analytics class
    Provides methods to retrieve and analyze SES metrics
    """
    
    def __init__(self):
        self.region = getattr(settings, 'AWS_SES_REGION', 'eu-west-1')
        self.session = boto3.Session(
            aws_access_key_id=getattr(settings, 'AWS_ACCESS_KEY_ID', None),
            aws_secret_access_key=getattr(settings, 'AWS_SECRET_ACCESS_KEY', None),
            region_name=self.region
        )
        self.ses_client = self.session.client('ses')
        self.cloudwatch_client = self.session.client('cloudwatch')
    
    def get_send_quota(self) -> Dict[str, Any]:
        """
        Get current SES sending quota and usage
        
        Returns:
            Dict containing quota information
        """
        try:
            quota = self.ses_client.get_send_quota()
            return {
                'max_24_hour_send': quota['Max24HourSend'],
                'max_send_rate': quota['MaxSendRate'],
                'sent_last_24h': quota['SentLast24Hours'],
                'remaining_quota': quota['Max24HourSend'] - quota['SentLast24Hours'],
                'quota_usage_percent': (quota['SentLast24Hours'] / quota['Max24HourSend']) * 100
            }
        except (ClientError, BotoCoreError) as e:
            logger.error(f"Failed to get SES send quota: {e}")
            return {}
    
    def get_send_statistics(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Get SES sending statistics for the specified number of days
        
        Args:
            days: Number of days to retrieve statistics for
            
        Returns:
            List of statistics data points
        """
        try:
            stats = self.ses_client.get_send_statistics()
            
            # Filter to last N days
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            filtered_stats = [
                stat for stat in stats['SendDataPoints']
                if stat['Timestamp'].replace(tzinfo=None) >= cutoff_date
            ]
            
            # Calculate additional metrics
            for stat in filtered_stats:
                total_sent = stat.get('DeliveryAttempts', 0)
                if total_sent > 0:
                    stat['bounce_rate'] = (stat.get('Bounces', 0) / total_sent) * 100
                    stat['complaint_rate'] = (stat.get('Complaints', 0) / total_sent) * 100
                    stat['reject_rate'] = (stat.get('Rejects', 0) / total_sent) * 100
                else:
                    stat['bounce_rate'] = 0
                    stat['complaint_rate'] = 0
                    stat['reject_rate'] = 0
            
            return sorted(filtered_stats, key=lambda x: x['Timestamp'], reverse=True)
            
        except (ClientError, BotoCoreError) as e:
            logger.error(f"Failed to get SES send statistics: {e}")
            return []
    
    def get_reputation_metrics(self) -> Dict[str, Any]:
        """
        Get SES reputation metrics from CloudWatch
        
        Returns:
            Dict containing reputation metrics
        """
        try:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(days=7)
            
            # Get reputation metrics from CloudWatch
            metrics = {}
            
            # Reputation.BounceRate
            bounce_rate = self._get_cloudwatch_metric(
                'AWS/SES', 'Reputation.BounceRate', start_time, end_time
            )
            if bounce_rate:
                metrics['bounce_rate'] = bounce_rate
            
            # Reputation.ComplaintRate
            complaint_rate = self._get_cloudwatch_metric(
                'AWS/SES', 'Reputation.ComplaintRate', start_time, end_time
            )
            if complaint_rate:
                metrics['complaint_rate'] = complaint_rate
            
            return metrics
            
        except (ClientError, BotoCoreError) as e:
            logger.error(f"Failed to get reputation metrics: {e}")
            return {}
    
    def _get_cloudwatch_metric(self, namespace: str, metric_name: str, 
                              start_time: datetime, end_time: datetime) -> Optional[float]:
        """
        Get a specific CloudWatch metric value
        
        Args:
            namespace: CloudWatch namespace
            metric_name: Name of the metric
            start_time: Start time for metric query
            end_time: End time for metric query
            
        Returns:
            Latest metric value or None
        """
        try:
            response = self.cloudwatch_client.get_metric_statistics(
                Namespace=namespace,
                MetricName=metric_name,
                StartTime=start_time,
                EndTime=end_time,
                Period=3600,  # 1 hour periods
                Statistics=['Average']
            )
            
            if response['Datapoints']:
                # Return the most recent value
                latest = max(response['Datapoints'], key=lambda x: x['Timestamp'])
                return latest['Average']
            
            return None
            
        except (ClientError, BotoCoreError) as e:
            logger.error(f"Failed to get CloudWatch metric {metric_name}: {e}")
            return None
    
    def get_verified_identities(self) -> Dict[str, List[str]]:
        """
        Get list of verified email addresses and domains
        
        Returns:
            Dict with 'emails' and 'domains' lists
        """
        try:
            identities = self.ses_client.list_verified_email_addresses()
            domains = self.ses_client.list_identities(IdentityType='Domain')
            
            return {
                'emails': identities.get('VerifiedEmailAddresses', []),
                'domains': domains.get('Identities', [])
            }
            
        except (ClientError, BotoCoreError) as e:
            logger.error(f"Failed to get verified identities: {e}")
            return {'emails': [], 'domains': []}
    
    def check_domain_verification(self, domain: str) -> Dict[str, Any]:
        """
        Check verification status of a domain
        
        Args:
            domain: Domain name to check
            
        Returns:
            Dict containing verification status and attributes
        """
        try:
            # Get verification attributes
            response = self.ses_client.get_identity_verification_attributes(
                Identities=[domain]
            )
            
            if domain in response['VerificationAttributes']:
                attrs = response['VerificationAttributes'][domain]
                return {
                    'verification_status': attrs.get('VerificationStatus'),
                    'verification_token': attrs.get('VerificationToken'),
                    'is_verified': attrs.get('VerificationStatus') == 'Success'
                }
            
            return {'is_verified': False, 'verification_status': 'NotStarted'}
            
        except (ClientError, BotoCoreError) as e:
            logger.error(f"Failed to check domain verification for {domain}: {e}")
            return {'is_verified': False, 'error': str(e)}
    
    def get_dkim_attributes(self, domain: str) -> Dict[str, Any]:
        """
        Get DKIM attributes for a domain
        
        Args:
            domain: Domain name to check
            
        Returns:
            Dict containing DKIM status and tokens
        """
        try:
            response = self.ses_client.get_identity_dkim_attributes(
                Identities=[domain]
            )
            
            if domain in response['DkimAttributes']:
                attrs = response['DkimAttributes'][domain]
                return {
                    'dkim_enabled': attrs.get('DkimEnabled', False),
                    'dkim_verification_status': attrs.get('DkimVerificationStatus'),
                    'dkim_tokens': attrs.get('DkimTokens', []),
                    'is_dkim_verified': attrs.get('DkimVerificationStatus') == 'Success'
                }
            
            return {'dkim_enabled': False}
            
        except (ClientError, BotoCoreError) as e:
            logger.error(f"Failed to get DKIM attributes for {domain}: {e}")
            return {'dkim_enabled': False, 'error': str(e)}
    
    def get_comprehensive_status(self) -> Dict[str, Any]:
        """
        Get comprehensive SES status including quotas, statistics, and verification
        
        Returns:
            Dict containing all SES status information
        """
        cache_key = 'ses_comprehensive_status'
        cached_status = cache.get(cache_key)
        
        if cached_status:
            return cached_status
        
        status = {
            'timestamp': datetime.utcnow().isoformat(),
            'quota': self.get_send_quota(),
            'statistics': self.get_send_statistics(days=7),
            'reputation': self.get_reputation_metrics(),
            'identities': self.get_verified_identities(),
            'region': self.region
        }
        
        # Check domain verification for strafrecht-online.org
        domain = 'strafrecht-online.org'
        status['domain_verification'] = self.check_domain_verification(domain)
        status['dkim_status'] = self.get_dkim_attributes(domain)
        
        # Calculate summary metrics
        if status['statistics']:
            recent_stats = status['statistics'][:7]  # Last 7 data points
            total_sent = sum(stat.get('DeliveryAttempts', 0) for stat in recent_stats)
            total_bounces = sum(stat.get('Bounces', 0) for stat in recent_stats)
            total_complaints = sum(stat.get('Complaints', 0) for stat in recent_stats)
            
            if total_sent > 0:
                status['summary'] = {
                    'total_sent_7_days': total_sent,
                    'avg_bounce_rate': (total_bounces / total_sent) * 100,
                    'avg_complaint_rate': (total_complaints / total_sent) * 100,
                    'health_status': self._calculate_health_status(
                        (total_bounces / total_sent) * 100,
                        (total_complaints / total_sent) * 100
                    )
                }
        
        # Cache for 5 minutes
        cache.set(cache_key, status, 300)
        
        return status
    
    def _calculate_health_status(self, bounce_rate: float, complaint_rate: float) -> str:
        """
        Calculate overall health status based on bounce and complaint rates
        
        Args:
            bounce_rate: Bounce rate percentage
            complaint_rate: Complaint rate percentage
            
        Returns:
            Health status string
        """
        # AWS SES thresholds
        if bounce_rate > 10 or complaint_rate > 0.5:
            return 'critical'
        elif bounce_rate > 5 or complaint_rate > 0.1:
            return 'warning'
        else:
            return 'healthy'


def get_ses_monitor() -> SESMonitor:
    """
    Get SES monitor instance
    
    Returns:
        SESMonitor instance
    """
    return SESMonitor()


def log_ses_metrics():
    """
    Log current SES metrics to the application log
    Useful for scheduled monitoring tasks
    """
    try:
        monitor = get_ses_monitor()
        status = monitor.get_comprehensive_status()
        
        logger.info(f"SES Status Report:")
        logger.info(f"  Quota Usage: {status['quota'].get('quota_usage_percent', 0):.1f}%")
        logger.info(f"  Remaining Quota: {status['quota'].get('remaining_quota', 0)}")
        
        if 'summary' in status:
            summary = status['summary']
            logger.info(f"  7-day Bounce Rate: {summary['avg_bounce_rate']:.2f}%")
            logger.info(f"  7-day Complaint Rate: {summary['avg_complaint_rate']:.2f}%")
            logger.info(f"  Health Status: {summary['health_status']}")
        
        domain_status = status.get('domain_verification', {})
        logger.info(f"  Domain Verified: {domain_status.get('is_verified', False)}")
        
        dkim_status = status.get('dkim_status', {})
        logger.info(f"  DKIM Enabled: {dkim_status.get('dkim_enabled', False)}")
        
    except Exception as e:
        logger.error(f"Failed to log SES metrics: {e}")
