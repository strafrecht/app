"""
Management command to check AWS SES status and metrics
Usage: python manage.py ses_status [--detailed] [--json]
"""

import json
from django.core.management.base import BaseCommand
from emails.utils.ses_monitoring import get_ses_monitor


class Command(BaseCommand):
    help = 'Check AWS SES status, quotas, and delivery metrics'

    def add_arguments(self, parser):
        parser.add_argument(
            '--detailed',
            action='store_true',
            help='Show detailed statistics and metrics'
        )
        parser.add_argument(
            '--json',
            action='store_true',
            help='Output results in JSON format'
        )
        parser.add_argument(
            '--days',
            type=int,
            default=7,
            help='Number of days for statistics (default: 7)'
        )

    def handle(self, *args, **options):
        try:
            monitor = get_ses_monitor()
            
            if options['detailed']:
                status = monitor.get_comprehensive_status()
            else:
                status = {
                    'quota': monitor.get_send_quota(),
                    'identities': monitor.get_verified_identities(),
                    'domain_verification': monitor.check_domain_verification('strafrecht-online.org'),
                    'dkim_status': monitor.get_dkim_attributes('strafrecht-online.org')
                }
            
            if options['json']:
                # Output as JSON
                self.stdout.write(json.dumps(status, indent=2, default=str))
            else:
                # Human-readable output
                self._display_status(status, options['detailed'])
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Failed to get SES status: {e}")
            )

    def _display_status(self, status, detailed=False):
        """Display status in human-readable format"""
        
        self.stdout.write(self.style.SUCCESS("📧 AWS SES Status Report"))
        self.stdout.write("=" * 50)
        
        # Quota Information
        if 'quota' in status and status['quota']:
            quota = status['quota']
            self.stdout.write("\n📊 Sending Quota:")
            self.stdout.write(f"  • Max 24h Send: {quota.get('max_24_hour_send', 'N/A')}")
            self.stdout.write(f"  • Max Send Rate: {quota.get('max_send_rate', 'N/A')} emails/second")
            self.stdout.write(f"  • Sent Last 24h: {quota.get('sent_last_24h', 'N/A')}")
            self.stdout.write(f"  • Remaining: {quota.get('remaining_quota', 'N/A')}")
            
            usage_percent = quota.get('quota_usage_percent', 0)
            if usage_percent > 80:
                usage_style = self.style.ERROR
                usage_icon = "🔴"
            elif usage_percent > 60:
                usage_style = self.style.WARNING
                usage_icon = "🟡"
            else:
                usage_style = self.style.SUCCESS
                usage_icon = "🟢"
            
            self.stdout.write(f"  • Usage: {usage_style(f'{usage_icon} {usage_percent:.1f}%')}")
        
        # Domain Verification
        if 'domain_verification' in status:
            domain_status = status['domain_verification']
            self.stdout.write("\n🌐 Domain Verification:")
            
            if domain_status.get('is_verified'):
                self.stdout.write(f"  • strafrecht-online.org: {self.style.SUCCESS('✅ Verified')}")
            else:
                verification_status = domain_status.get('verification_status', 'Unknown')
                self.stdout.write(f"  • strafrecht-online.org: {self.style.ERROR(f'❌ {verification_status}')}")
                
                if 'verification_token' in domain_status:
                    self.stdout.write(f"  • Verification Token: {domain_status['verification_token']}")
        
        # DKIM Status
        if 'dkim_status' in status:
            dkim = status['dkim_status']
            self.stdout.write("\n🔐 DKIM Configuration:")
            
            if dkim.get('dkim_enabled'):
                if dkim.get('is_dkim_verified'):
                    self.stdout.write(f"  • DKIM: {self.style.SUCCESS('✅ Enabled and Verified')}")
                else:
                    dkim_status = dkim.get('dkim_verification_status', 'Unknown')
                    self.stdout.write(f"  • DKIM: {self.style.WARNING(f'🟡 Enabled but {dkim_status}')}")
                
                if dkim.get('dkim_tokens'):
                    self.stdout.write("  • DKIM Tokens:")
                    for i, token in enumerate(dkim['dkim_tokens'][:3]):  # Show first 3
                        self.stdout.write(f"    {i+1}. {token}")
            else:
                self.stdout.write(f"  • DKIM: {self.style.ERROR('❌ Not Enabled')}")
        
        # Verified Identities
        if 'identities' in status:
            identities = status['identities']
            self.stdout.write("\n📋 Verified Identities:")
            
            if identities.get('domains'):
                self.stdout.write("  • Domains:")
                for domain in identities['domains']:
                    self.stdout.write(f"    - {domain}")
            
            if identities.get('emails'):
                self.stdout.write("  • Email Addresses:")
                for email in identities['emails'][:5]:  # Show first 5
                    self.stdout.write(f"    - {email}")
                if len(identities['emails']) > 5:
                    self.stdout.write(f"    ... and {len(identities['emails']) - 5} more")
        
        # Detailed Statistics
        if detailed and 'statistics' in status:
            self._display_detailed_statistics(status)
        
        # Summary Health Status
        if 'summary' in status:
            summary = status['summary']
            self.stdout.write("\n🏥 Health Summary (Last 7 Days):")
            self.stdout.write(f"  • Total Sent: {summary.get('total_sent_7_days', 0)}")
            self.stdout.write(f"  • Avg Bounce Rate: {summary.get('avg_bounce_rate', 0):.2f}%")
            self.stdout.write(f"  • Avg Complaint Rate: {summary.get('avg_complaint_rate', 0):.2f}%")
            
            health_status = summary.get('health_status', 'unknown')
            if health_status == 'healthy':
                health_display = self.style.SUCCESS('🟢 Healthy')
            elif health_status == 'warning':
                health_display = self.style.WARNING('🟡 Warning')
            elif health_status == 'critical':
                health_display = self.style.ERROR('🔴 Critical')
            else:
                health_display = '❓ Unknown'
            
            self.stdout.write(f"  • Overall Status: {health_display}")
        
        self.stdout.write("\n" + "=" * 50)

    def _display_detailed_statistics(self, status):
        """Display detailed sending statistics"""
        statistics = status.get('statistics', [])
        
        if not statistics:
            self.stdout.write("\n📈 No recent statistics available")
            return
        
        self.stdout.write("\n📈 Detailed Statistics (Recent):")
        self.stdout.write("  Date/Time           | Sent | Bounces | Complaints | Rejects")
        self.stdout.write("  " + "-" * 65)
        
        for stat in statistics[:10]:  # Show last 10 data points
            timestamp = stat['Timestamp'].strftime('%Y-%m-%d %H:%M')
            sent = stat.get('DeliveryAttempts', 0)
            bounces = stat.get('Bounces', 0)
            complaints = stat.get('Complaints', 0)
            rejects = stat.get('Rejects', 0)
            
            self.stdout.write(
                f"  {timestamp:19} | {sent:4} | {bounces:7} | {complaints:10} | {rejects:7}"
            )
        
        # Reputation metrics
        if 'reputation' in status and status['reputation']:
            reputation = status['reputation']
            self.stdout.write("\n🎯 Reputation Metrics:")
            
            if 'bounce_rate' in reputation:
                bounce_rate = reputation['bounce_rate']
                if bounce_rate > 10:
                    bounce_style = self.style.ERROR
                elif bounce_rate > 5:
                    bounce_style = self.style.WARNING
                else:
                    bounce_style = self.style.SUCCESS
                self.stdout.write(f"  • Bounce Rate: {bounce_style(f'{bounce_rate:.2f}%')}")
            
            if 'complaint_rate' in reputation:
                complaint_rate = reputation['complaint_rate']
                if complaint_rate > 0.5:
                    complaint_style = self.style.ERROR
                elif complaint_rate > 0.1:
                    complaint_style = self.style.WARNING
                else:
                    complaint_style = self.style.SUCCESS
                self.stdout.write(f"  • Complaint Rate: {complaint_style(f'{complaint_rate:.2f}%')}")
