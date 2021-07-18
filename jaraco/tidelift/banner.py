from importlib_resources import files

from docutils.parsers import rst
from docutils.nodes import raw


class ReferralBanner(rst.Directive):
    def run(self):
        template = files(__package__).joinpath('banner.html').read_text()
        content = template.replace('{{ project }}', self.app.config.project)
        return [raw('', content, format='html')]


def setup(app):
    app.add_directive('tidelift-referral-banner', ReferralBanner)
    ReferralBanner.app = app
