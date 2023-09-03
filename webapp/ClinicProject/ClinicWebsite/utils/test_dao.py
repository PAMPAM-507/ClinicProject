from ClinicWebsite.models import News
from ClinicWebsite.utils.dao.queries.all_query import AllQuery

# AllQuery().all_query(News)

print(News.objects.all())
