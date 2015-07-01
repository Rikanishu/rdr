# encoding: utf-8

from rdr.application.static import manager
from static_bundle import (JsBundle,
                           CssBundle,
                           OtherFilesBundle,
                           LessCompilerPrepareHandler)

css1 = CssBundle("css")
css1.add_file("fonts.css")
css1.add_file("bootstrap/bootstrap.css")
css1.add_file("bootstrap-theme/theme.css")
css1.add_file("font-awesome/font-awesome.css")
css1.add_file("nvd3/nv.d3.css")
css1.add_file("upload/btn-upload.less")
css1.add_file("app/style.less")
css1.add_file("app/feeds.less")
css1.add_file("app/stats.less")
css1.add_file("app/manage.less")
css1.add_file("app/dashboard.less")
css1.add_file("app/settings.less")
css1.add_file("app/offline-queue.less")
css1.add_prepare_handler(LessCompilerPrepareHandler(output_dir="compiled"))

js1 = JsBundle("js")
js1.add_file("vendors/jquery-1.10.2/jquery.js")
js1.add_file("vendors/angular/angular.js")
js1.add_file("vendors/bootstrap/bootstrap.js")
js1.add_file("vendors/angular-ui-router/angular-ui-router.js")
js1.add_file("vendors/angular-ui-bootstrap/angular-ui-bootstrap.js")
js1.add_file("vendors/ng-draggable/ngDraggable.js")
js1.add_file("vendors/d3/d3.js")
js1.add_file("vendors/nvd3/nv.d3.js")
js1.add_file("vendors/angular-nvd3/angularjs-nvd3-directives.js")
js1.add_file("vendors/angular-upload/angular-upload.js")
js1.add_file("vendors/angular-hotkeys/angular-hotkeys.js")

js2 = JsBundle("js/modules")

fonts = OtherFilesBundle("fonts")
images = OtherFilesBundle("img")
partials = OtherFilesBundle("js/partials")

builder = manager.create_builder()
builder.create_asset("MainStyles", minify=True).add_bundle(css1)
builder.create_asset("MainScripts", minify=True, merge=True).add_bundle(js1)
builder.create_asset("AngularModules", minify=True, merge=True).add_bundle(js2)
builder.create_asset("AllOtherFiles").add_bundle(fonts, images, partials)
