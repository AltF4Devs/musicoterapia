from django.contrib import admin
from users.models import User
from base.models import Checklist


class ChecklistInline(admin.TabularInline):
    model = Checklist
    readonly_fields = ('playlist', 'date', 'display_music_count', 'completed')
    exclude = ('time_elapsed',)
    show_change_link = True
    can_delete = False
    extra = 1


class UserAdmin(admin.ModelAdmin):
    inlines = [ChecklistInline]

    list_display = ('email', 'full_name', 'music_group', 'week', 'complete_treatment')
    list_filter = ('complete_treatment', 'music_group', 'week')

    fieldsets = (
        (None, {'fields': ('email', 'full_name', 'date_joined', 'is_active')}),
        (
            'Pesquisa',
            {'fields': ('music_group', 'week', 'next_form', 'complete_treatment')},
        ),
    )
    readonly_fields = ('date_joined',)


# Register your models here.
admin.site.register(User, UserAdmin)
