import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from ..models import Tenant

User = get_user_model()


class TenantModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
    
    def test_create_tenant(self):
        """Test creating a tenant"""
        tenant = Tenant.objects.create(
            name="Test Tenant",
            slug="test-tenant",
            contact_email="admin@test-tenant.com",
            max_users=10,
            created_by=self.user
        )
        
        self.assertEqual(tenant.name, "Test Tenant")
        self.assertEqual(tenant.slug, "test-tenant")
        self.assertTrue(tenant.is_active)
        self.assertEqual(tenant.max_users, 10)
        self.assertEqual(tenant.user_count, 0)
        self.assertFalse(tenant.is_at_user_limit)
    
    def test_tenant_string_representation(self):
        """Test tenant string representation"""
        tenant = Tenant.objects.create(
            name="Test Tenant",
            slug="test-tenant",
            created_by=self.user
        )
        self.assertEqual(str(tenant), "Test Tenant")
    
    def test_tenant_user_count(self):
        """Test tenant user count property"""
        tenant = Tenant.objects.create(
            name="Test Tenant",
            slug="test-tenant",
            created_by=self.user
        )
        
        # Initially 0 users
        self.assertEqual(tenant.user_count, 0)
        
        # Note: In a real implementation, you'd associate users with tenants
        # This is a placeholder for when that relationship is established


class TenantAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123'
        )
        self.tenant_data = {
            'name': 'Test Tenant',
            'slug': 'test-tenant',
            'contact_email': 'admin@test-tenant.com',
            'max_users': 20
        }
    
    def test_list_tenants_authenticated(self):
        """Test listing tenants as authenticated user"""
        self.client.force_authenticate(user=self.user)
        Tenant.objects.create(
            name="Test Tenant",
            slug="test-tenant",
            created_by=self.user
        )
        
        response = self.client.get('/api/v1/tenants/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_list_tenants_unauthenticated(self):
        """Test listing tenants without authentication"""
        response = self.client.get('/api/v1/tenants/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_tenant_as_admin(self):
        """Test creating tenant as admin user"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post('/api/v1/tenants/', self.tenant_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Tenant.objects.filter(slug='test-tenant').exists())
    
    def test_create_tenant_as_regular_user(self):
        """Test creating tenant as regular user (should fail)"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/v1/tenants/', self.tenant_data)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_tenant_stats(self):
        """Test getting tenant statistics"""
        self.client.force_authenticate(user=self.user)
        tenant = Tenant.objects.create(
            name="Test Tenant",
            slug="test-tenant",
            max_users=10,
            created_by=self.user
        )
        
        response = self.client.get(f'/api/v1/tenants/{tenant.id}/stats/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user_count', response.data)
        self.assertIn('max_users', response.data)
        self.assertIn('is_at_user_limit', response.data)
    
    def test_activate_tenant(self):
        """Test activating a tenant"""
        self.client.force_authenticate(user=self.admin_user)
        tenant = Tenant.objects.create(
            name="Test Tenant",
            slug="test-tenant",
            is_active=False,
            created_by=self.user
        )
        
        response = self.client.post(f'/api/v1/tenants/{tenant.id}/activate/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        tenant.refresh_from_db()
        self.assertTrue(tenant.is_active)