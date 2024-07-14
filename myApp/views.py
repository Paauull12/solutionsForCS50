from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import requests
#from secret import TOKEN

def get_repo_tree(repo_url, branch='main'):
    api_url = f"https://api.github.com/repos/{repo_url}/git/trees/{branch}?recursive=1"

    headers = {
        'Authorization': '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'
    }

    response = requests.get(api_url, headers=headers)

    #response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        tree = data.get('tree', [])

        structure = {}
        for item in tree:
            path_parts = item['path'].split('/')
            current_level = structure
            for part in path_parts:
                if part == path_parts[-1]:  # Last part, determine if file or dir
                    if item['type'] == 'blob':
                        current_level[part] = 'file'
                    else:
                        current_level[part] = {}
                else:
                    if part not in current_level:
                        current_level[part] = {}
                    current_level = current_level[part]

        return structure
    else:
        return {}

def get_folder_details(request):
    folder_name = request.GET.get('folder_name')
    repo_url = "Paauull12/cs50"

    tree = get_repo_tree(repo_url)

    parts = folder_name.split('/')
    current_level = tree
    for part in parts:
        if part in current_level:
            current_level = current_level[part]
        else:
            return JsonResponse({'error': 'Folder not found'}, status=404)

    files = [name for name, type_ in current_level.items() if type_ == 'file' or isinstance(type_, dict)]



    return JsonResponse({'files': files})





def get_file_content(request):
    folder_name = request.GET.get('folder_name')
    file_name = request.GET.get('file_name')
    repo_url = f"https://raw.githubusercontent.com/Paauull12/cs50/main/{folder_name}/{file_name}"

    response = requests.get(repo_url)

    if response.status_code == 200:
        return HttpResponse(response.text, content_type='text/plain')
    else:
        return JsonResponse({'error': 'File not found'}, status=404)

def home(request):
    repo_url = "Paauull12/cs50"
    tree_structure = get_repo_tree(repo_url)

    context = {
        'tree': tree_structure,
    }
    return render(request, 'home.html', context)
