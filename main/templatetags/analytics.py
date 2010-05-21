from django import template
import settings
register = template.Library()


class ShowGoogleAnalyticsJS(template.Node):
	def render(self, context):
		code =  getattr(settings, "GOOGLE_ANALYTICS_CODE", False)
		if not code:
			return "<!-- Goggle Analytics not included because you haven't set the settings.GOOGLE_ANALYTICS_CODE variable! -->"

		if 'user' in context and context['user'] and context['user'].is_staff:
			return "<!-- Goggle Analytics not included because you are a staff user! -->"

		if settings.DEBUG:
			return "<!-- Goggle Analytics not included because you are in Debug mode! -->"

		return """
		<script type="text/javascript">
			var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
			document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
		</script>
		<script type="text/javascript">
			try {
			var pageTracker = _gat._getTracker('""" + str(code) + """');
			pageTracker._trackPageview();
		} catch(err) {}</script>
		"""

def googleanalyticsjs(parser, token):
	return ShowGoogleAnalyticsJS()

show_common_data = register.tag(googleanalyticsjs)
