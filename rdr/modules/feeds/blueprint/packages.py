# encoding: utf-8

from rdr.modules.feeds.blueprint import blueprint
from rdr.components.helpers import json
from rdr.modules.users.session import login_required

@blueprint.route('/packages/resolve', methods=['POST'])
@json.wrap
@login_required
def resolve_packages():
    body = json.get_request_body()
    query = body['query']
    if not query:
        raise json.InvalidRequest("Invalid query format")
    from rdr.modules.feeds.packages.resolver import PackagesResolver

    packages = PackagesResolver(query).run().result_dict()

    return {
        'success': True,
        'packages': packages
    }

@blueprint.route('/packages/popular')
@json.wrap
@login_required
def popular_packages():
    from rdr.modules.home.dashboard.packages import PopularPackagesGenerator
    from rdr.modules.feeds.articles.status import UserPackageRecord

    gen = PopularPackagesGenerator(packages_count=12)
    package_records = UserPackageRecord.wrap_packages_list(gen.fetch_packages())
    return {
        'success': True,
        'popularPackages': [x.to_dict() for x in package_records]
    }
