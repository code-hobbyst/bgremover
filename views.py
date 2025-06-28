from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.files.base import ContentFile
from .models import ProcessedImage
from .bg_processor import remove_white_background, smart_transparency
import io
import os

def home(request):
    """Home page with upload form"""
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            # Save uploaded image
            uploaded_file = request.FILES['image']
            processed_image = ProcessedImage(original_image=uploaded_file)
            processed_image.save()
            
            # Process the image
            original_path = processed_image.original_image.path
            
            # Choose processing method
            method = request.POST.get('method', 'white')
            
            if method == 'smart':
                result_img = smart_transparency(original_path)
            else:
                result_img = remove_white_background(original_path)
            
            # Save processed image
            img_io = io.BytesIO()
            result_img.save(img_io, format='PNG')
            img_content = ContentFile(img_io.getvalue())
            
            # Generate filename
            original_name = os.path.splitext(uploaded_file.name)[0]
            processed_filename = f"processed_{original_name}.png"
            
            processed_image.processed_image.save(
                processed_filename,
                img_content,
                save=True
            )
            
            messages.success(request, 'Background removed successfully!')
            return redirect('result', pk=processed_image.pk)
            
        except Exception as e:
            messages.error(request, f'Error processing image: {str(e)}')
    
    # Get recent images
    recent_images = ProcessedImage.objects.filter(processed_image__isnull=False)[:6]
    
    return render(request, 'home.html', {'recent_images': recent_images})

def result(request, pk):
    """Show result"""
    processed_image = get_object_or_404(ProcessedImage, pk=pk)
    return render(request, 'result.html', {'processed_image': processed_image})

def gallery(request):
    """Gallery view"""
    images = ProcessedImage.objects.filter(processed_image__isnull=False)
    return render(request, 'gallery.html', {'images': images})