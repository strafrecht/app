"""
Management command to set up Wagtail sites for development and production
Usage: python manage.py setup_sites
"""

from django.core.management.base import BaseCommand
from django.conf import settings
from wagtail.models import Site, Page


class Command(BaseCommand):
    help = 'Set up Wagtail sites for development and production environments'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force update existing site configurations'
        )

    def handle(self, *args, **options):
        try:
            # Get the root page
            root_page = Page.objects.filter(depth=1).first()
            if not root_page:
                self.stdout.write(
                    self.style.ERROR("❌ No root page found. Please run migrations first.")
                )
                return

            # Determine if we're in development mode
            is_debug = getattr(settings, 'DEBUG', False)
            site_url = getattr(settings, 'SITE_URL', 'http://localhost:8000')
            
            self.stdout.write(f"🔧 Setting up sites (DEBUG={is_debug}, SITE_URL={site_url})")

            if is_debug:
                self._setup_development_site(root_page, options['force'])
            else:
                self._setup_production_site(root_page, options['force'])

            self.stdout.write(self.style.SUCCESS("✅ Site configuration completed"))

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Failed to set up sites: {e}")
            )

    def _setup_development_site(self, root_page, force=False):
        """Set up development site configuration"""

        # Try to find the actual HomePage instead of using root page
        from pages.models.home import HomePage
        try:
            home_page = HomePage.objects.first()
            if home_page:
                site_root_page = home_page
                self.stdout.write(f"🏠 Using HomePage: {home_page.title} (ID: {home_page.id})")
            else:
                site_root_page = root_page
                self.stdout.write(f"⚠️  No HomePage found, using root page: {root_page.title}")
        except Exception as e:
            site_root_page = root_page
            self.stdout.write(f"⚠️  Error finding HomePage: {e}, using root page")

        # Create or update localhost site
        dev_site, created = Site.objects.get_or_create(
            hostname='localhost',
            port=8000,
            defaults={
                'site_name': 'Strafrecht Online (Development)',
                'root_page': site_root_page,
                'is_default_site': True
            }
        )

        if created:
            self.stdout.write("🆕 Created development site: localhost:8000")
        elif force:
            dev_site.site_name = 'Strafrecht Online (Development)'
            dev_site.root_page = site_root_page
            dev_site.is_default_site = True
            dev_site.save()
            self.stdout.write("🔄 Updated development site: localhost:8000")
        else:
            self.stdout.write("ℹ️  Development site already exists: localhost:8000")
            # Check if we need to update the root page even without force
            if dev_site.root_page != site_root_page:
                dev_site.root_page = site_root_page
                dev_site.save()
                self.stdout.write(f"🔄 Updated root page to: {site_root_page.title}")

        # Make sure development site is default
        if not dev_site.is_default_site:
            dev_site.is_default_site = True
            dev_site.save()
            self.stdout.write("✅ Set development site as default")

        # Make production site non-default if it exists
        prod_sites = Site.objects.filter(hostname='strafrecht-online.org')
        for prod_site in prod_sites:
            if prod_site.is_default_site:
                prod_site.is_default_site = False
                prod_site.save()
                self.stdout.write("🔄 Set production site as non-default")

        # Ensure development site has menu items
        self._ensure_dev_menu_items(dev_site, force)

    def _ensure_dev_menu_items(self, dev_site, force=False):
        """Ensure development site has menu items copied from production"""
        try:
            from wagtailmenus.models import MainMenu, MainMenuItem

            # Get or create development menu
            dev_menu, created = MainMenu.objects.get_or_create(
                site=dev_site,
                defaults={'max_levels': 3}
            )

            # Check if dev menu has items
            dev_items_count = MainMenuItem.objects.filter(menu=dev_menu).count()

            if dev_items_count == 0 or force:
                # Try to copy from production site
                prod_site = Site.objects.filter(hostname='strafrecht-online.org').first()
                if prod_site:
                    try:
                        prod_menu = MainMenu.objects.get(site=prod_site)
                        prod_items = MainMenuItem.objects.filter(menu=prod_menu).order_by('sort_order')

                        if prod_items.exists():
                            # Clear existing dev menu items if force
                            if force:
                                MainMenuItem.objects.filter(menu=dev_menu).delete()

                            # Copy items
                            copied_count = 0
                            for prod_item in prod_items:
                                if not MainMenuItem.objects.filter(
                                    menu=dev_menu,
                                    link_page=prod_item.link_page,
                                    link_url=prod_item.link_url
                                ).exists():
                                    MainMenuItem.objects.create(
                                        menu=dev_menu,
                                        link_page=prod_item.link_page,
                                        link_url=prod_item.link_url,
                                        link_text=prod_item.link_text,
                                        sort_order=prod_item.sort_order,
                                        allow_subnav=prod_item.allow_subnav
                                    )
                                    copied_count += 1

                            if copied_count > 0:
                                self.stdout.write(f"📋 Copied {copied_count} menu items from production to development")
                            else:
                                self.stdout.write("ℹ️  Development menu items already up to date")
                        else:
                            self.stdout.write("⚠️  No menu items found in production site to copy")
                    except MainMenu.DoesNotExist:
                        self.stdout.write("⚠️  No MainMenu found for production site")
                else:
                    self.stdout.write("⚠️  Production site not found, cannot copy menu items")
            else:
                self.stdout.write(f"✅ Development site already has {dev_items_count} menu items")

        except ImportError:
            self.stdout.write("⚠️  wagtailmenus not available, skipping menu setup")

    def _setup_production_site(self, root_page, force=False):
        """Set up production site configuration"""
        
        # Create or update production site
        prod_site, created = Site.objects.get_or_create(
            hostname='strafrecht-online.org',
            port=443,
            defaults={
                'site_name': 'Strafrecht Online',
                'root_page': root_page,
                'is_default_site': True
            }
        )

        if created:
            self.stdout.write("🆕 Created production site: strafrecht-online.org")
        elif force:
            prod_site.site_name = 'Strafrecht Online'
            prod_site.is_default_site = True
            prod_site.save()
            self.stdout.write("🔄 Updated production site: strafrecht-online.org")
        else:
            self.stdout.write("ℹ️  Production site already exists: strafrecht-online.org")

        # Make sure production site is default
        if not prod_site.is_default_site:
            prod_site.is_default_site = True
            prod_site.save()
            self.stdout.write("✅ Set production site as default")

        # Make development sites non-default if they exist
        dev_sites = Site.objects.filter(hostname='localhost')
        for dev_site in dev_sites:
            if dev_site.is_default_site:
                dev_site.is_default_site = False
                dev_site.save()
                self.stdout.write("🔄 Set development site as non-default")
