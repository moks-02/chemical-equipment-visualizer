from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.http import FileResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UploadedDataset
from .serializers import (
    UploadedDatasetSerializer,
    DatasetListSerializer,
    CSVUploadSerializer
)
from .utils import parse_csv_file, calculate_summary, dataframe_to_json
from .pdf_generator import generate_pdf_report
import io


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    User login endpoint.
    Accepts username and password, returns authentication token.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Please provide both username and password'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    
    if not user:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    token, created = Token.objects.get_or_create(user=user)
    
    return Response({
        'token': token.key,
        'user_id': user.id,
        'username': user.username
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def signup_view(request):
    """
    User signup endpoint.
    Accepts username, password, and optional email to create a new user.
    """
    from django.contrib.auth.models import User
    
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')
    
    if not username or not password:
        return Response(
            {'error': 'Please provide both username and password'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if username already exists
    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Validate password length
    if len(password) < 6:
        return Response(
            {'error': 'Password must be at least 6 characters long'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Create new user
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        
        # Create token for the new user
        token = Token.objects.create(user=user)
        
        return Response({
            'token': token.key,
            'username': user.username,
            'message': 'Account created successfully'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': f'Failed to create account: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_csv(request):
    """
    Upload and process CSV file.
    Returns parsed data and summary statistics.
    """
    serializer = CSVUploadSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    file = serializer.validated_data['file']
    
    try:
        # Parse CSV file
        df = parse_csv_file(file)
        
        # Calculate summary statistics
        summary = calculate_summary(df)
        
        # Convert DataFrame to JSON
        data_json = dataframe_to_json(df)
        
        # Save to database with user association
        dataset = UploadedDataset.objects.create(
            user=request.user,
            filename=file.name,
            file_path=file,
            summary_json=summary,
            data_json=data_json
        )
        
        # Serialize and return
        response_serializer = UploadedDatasetSerializer(dataset)
        
        return Response({
            'message': 'File uploaded and processed successfully',
            'dataset': response_serializer.data
        }, status=status.HTTP_201_CREATED)
    
    except ValueError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': f'An error occurred: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_datasets(request):
    """
    List all uploaded datasets for the current user (last 5).
    Returns lightweight data without full dataset content.
    """
    datasets = UploadedDataset.objects.filter(user=request.user).order_by('-upload_date')[:5]
    serializer = DatasetListSerializer(datasets, many=True)
    
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dataset_detail(request, pk):
    """
    Get detailed information about a specific dataset.
    Includes full data and summary. Only returns user's own datasets.
    """
    try:
        dataset = UploadedDataset.objects.get(pk=pk, user=request.user)
        serializer = UploadedDatasetSerializer(dataset)
        
        return Response(serializer.data)
    
    except UploadedDataset.DoesNotExist:
        return Response(
            {'error': 'Dataset not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def generate_report(request, pk):
    """
    Generate PDF report for a specific dataset.
    Returns PDF file for download. Only generates reports for user's own datasets.
    """
    try:
        dataset = UploadedDataset.objects.get(pk=pk, user=request.user)
        
        # Generate PDF
        pdf_buffer = generate_pdf_report(dataset)
        
        # Create response with PDF
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{dataset.filename}_report.pdf"'
        
        return response
    
    except UploadedDataset.DoesNotExist:
        return Response(
            {'error': 'Dataset not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': f'Error generating report: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def preview_report(request, pk):
    """
    Generate PDF report for preview (inline viewing in browser).
    Returns PDF file for inline display. Only previews user's own datasets.
    """
    try:
        dataset = UploadedDataset.objects.get(pk=pk, user=request.user)
        
        # Generate PDF
        pdf_buffer = generate_pdf_report(dataset)
        
        # Create response with PDF for inline viewing
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{dataset.filename}_report.pdf"'
        
        return response
    
    except UploadedDataset.DoesNotExist:
        return Response(
            {'error': 'Dataset not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': f'Error generating report: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_dataset(request, pk):
    """
    Delete a specific dataset. Only deletes user's own datasets.
    """
    try:
        dataset = UploadedDataset.objects.get(pk=pk, user=request.user)
        filename = dataset.filename
        dataset.delete()
        
        return Response({
            'message': f'Dataset "{filename}" deleted successfully'
        })
    
    except UploadedDataset.DoesNotExist:
        return Response(
            {'error': 'Dataset not found'},
            status=status.HTTP_404_NOT_FOUND
        )
