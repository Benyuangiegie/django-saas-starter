from django.db import models
from django.conf import settings
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel
import uuid


class BaseModel(SafeDeleteModel):
    """
    Base model with soft delete functionality and audit fields.
    All models should inherit from this or BaseModelWithTenant.
    """
    _safedelete_policy = SOFT_DELETE_CASCADE
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name="created_%(class)s_objects",
        on_delete=models.DO_NOTHING,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name="updated_%(class)s_objects",
        on_delete=models.DO_NOTHING,
    )

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class BaseModelWithTenant(BaseModel):
    """
    Base model with tenant support for multi-tenancy.
    Use this for models that need to be isolated by tenant.
    """
    tenant = models.ForeignKey(
        "tenants.Tenant", 
        blank=True,
        null=True,
        related_name="%(class)s_objects",
        on_delete=models.CASCADE,
        help_text="The tenant this record belongs to"
    )

    class Meta:
        abstract = True
        ordering = ["-created_at"]