from django.views.decorators.http import require_POST, require_http_methods
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from scrapyd_api import ScrapydAPI
from ebay.models import Product

# connect scrapyd service
scrapyd = ScrapydAPI('http://localhost:6800')

@csrf_exempt
@require_http_methods(['POST', 'GET']) # only get and post
def crawl(request):
    # Post requests are for new crawling tasks
    if request.method == 'POST':

        row = request.POST.get('row', None)

        # Here we schedule a new crawling task from scrapyd.
        # Notice that settings is a special argument name.
        # But we can pass other arguments, though.
        # This returns a ID which belongs and will be belong to this task
        # We are going to use that to check task's status.
        task = scrapyd.schedule('server', 'ebay', row=row)

        return JsonResponse({'task_id': task})

    elif request.method == 'GET':
        return JsonResponse({'error': 'Missing args'})