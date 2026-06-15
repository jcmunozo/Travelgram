"""Shared view mixins"""
#django
from django.http import JsonResponse
from django.template.loader import render_to_string


class AjaxableFormMixin:
    """Let an UpdateView/CreateView power a modal form.

    For XHR submits it returns JSON (a redirect URL on success, or the
    re-rendered form partial with errors on failure) so the page is never left.
    Plain (no-JS) submits keep Django's default redirect/render behaviour, so
    the standalone form pages still work as a fallback.
    """

    # Template fragment re-rendered (with errors) for invalid AJAX submits.
    ajax_partial = None

    def _is_ajax(self):
        return self.request.headers.get('x-requested-with') == 'XMLHttpRequest'

    def form_valid(self, form):
        response = super().form_valid(form)
        if self._is_ajax():
            return JsonResponse({'success': True, 'redirect': str(self.get_success_url())})
        return response

    def form_invalid(self, form):
        if self._is_ajax():
            html = render_to_string(
                self.ajax_partial,
                self.get_context_data(form=form),
                request=self.request,
            )
            return JsonResponse({'success': False, 'html': html}, status=400)
        return super().form_invalid(form)
