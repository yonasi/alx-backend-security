# ALX Backend Security: IP Tracking Module

## Overview

The `ip_tracking` module is a Django application designed to enhance web application security and analytics through IP tracking. It provides features for logging requests, blacklisting malicious IPs, geolocation analytics, rate limiting, and anomaly detection, all while considering privacy and compliance (e.g., GDPR/CCPA).

### Features
- **IP Logging**: Logs IP address, timestamp, path, country, and city for every request using middleware.
- **IP Blacklisting**: Blocks requests from specified IPs with a management command to add them.
 **Geolocation Analytics**: Enhances logs with country and city data, cached for 24 hours.
- **Rate Limiting**: Limits requests to sensitive views (e.g., login) to 5/min (anonymous) and 10/min (authenticated).
- **Anomaly Detection**: Flags suspicious IPs (e.g., >100 requests/hour or accessing sensitive paths) via an hourly Celery task.