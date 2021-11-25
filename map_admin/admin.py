from django.contrib import admin
from .models import Map

class MapAdmin(admin.ModelAdmin):
    change_list_template = 'map/map_change_list.html'
    list_filter = ['name',]
    search_fields = ['name']
    #list_filter = ( MarketCapFilter )

    # def market_cap_value(self, obj):
    #   return obj.market_cap_value > 1000000000

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
            print(qs)
        except (AttributeError, KeyError):
            return response

        metrics = {
            'total_volume': Sum('volume'),
            'total_mcap': Sum('market_cap'),
        }
        response.context_data['nf_200_list'] = list(
            qs
            .values('rank','ticker','name','priceUSD','market_cap','volume','change_24h')
           # .annotate(**metrics)
            .order_by('-market_cap')[:200]
        )

        response.context_data['nf_200_totals'] = dict(
            qs.aggregate(**metrics)
        )

        return response

admin.site.register(Map, MapAdmin)