import * as Sentry from "@sentry/browser";
import { Integrations } from "@sentry/tracing";

alert('here')

Sentry.init({
  dsn: "https://b43678e42cdf4f38a9b0dadf573da567@o244196.ingest.sentry.io/1723408",
  release: "frontend@" + process.env.npm_package_version, // To set your release version
  integrations: [new Integrations.BrowserTracing()],
  tracesSampleRate: 1.0, // We recommend adjusting this in production
});

console.log(kasfd)
