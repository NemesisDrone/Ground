# Sentry Error tracking

Sentry is an error tracking tool that helps you monitor and fix crashes in real time. It provides insights into the most
important errors in the application, and helps us understand the impact of each error.

## How to use Sentry

Connect to the [Sentry dashboard](https://nemesis-3p.sentry.io) using the credentials provided in Bitwarden.
In the issues tab, you can see all the errors that have been tracked by Sentry.

## Sentry configuration

Sentry is only configured on the backend. The configuration is done in the `backend/nemesis/settings-prod.py` file.
It is only enabled in the production environment.
Feel free to add Sentry to the frontend.
