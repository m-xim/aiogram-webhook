{% note warning "Configure request verification" %}

The engines work without `security=...`, but the library emits a warning because webhook endpoints are public HTTP routes.
Use a Telegram secret token, an IP check, or both for production deployments.

{% endnote %}
