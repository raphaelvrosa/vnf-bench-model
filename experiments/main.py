import logging
import os
from yaml import load
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from jinja2 import Environment, FileSystemLoader

LOG = logging.getLogger(os.path.basename(__file__))
coloredlogs.install(level="DEBUG")
setLogLevel('info')

from topo import Experiment


class TemplateParser:
    def __init__(self):
        self.tmp_configs = './vnf-br/templates/'

    def parse(self, input_filename, context):
        input_folder = self.tmp_configs
        output_folder = self.tmp_configs
        output_file = "parsed_" + input_filename
        rendered = self._render_template(input_filename, input_folder, context)
        template_output_path = self._full_path(output_folder)
        open(os.path.join(template_output_path, output_file), 'w').write(
            rendered.encode('utf8'))
        return output_file

    def load_file(self, output_file):
        template_output_path = self._full_path(self.tmp_configs)
        filename = os.path.join(template_output_path, output_file)
        data = {}
        try:
            with open(filename, 'r') as f:
                data = load(f, Loader=Loader)
        except Exception as e:
            logger.debug('exception: could not load outline file %s', e)
        finally:
            return data

    def _full_path(self, temp_dir):
        return os.path.normpath(
            os.path.join(
                os.path.dirname(__file__), temp_dir))

    def _render_template(self, template_file, temp_dir, context):
        j2_tmpl_path = self._full_path(temp_dir)
        j2_env = Environment(loader=FileSystemLoader(j2_tmpl_path))
        j2_tmpl = j2_env.get_template(template_file)
        rendered = j2_tmpl.render(dict(temp_dir=temp_dir, **context))
        return rendered.encode('utf8')


class Play:
    def __init__(self):
        self.experiments = {}
        self.template_filename = ""
        self.inputs = {}
        self.parser = TemplateParser()
        self.exp_topo = None

    def create_exp_topo(self, template_filename, inputs):
        exp_template_out_filename = self.parser.parse(template_filename, inputs)
        exp_template = self.parser.load_file(exp_template_out_filename)
        _id = exp_template.get("id")
        _name = exp_template.get("name")
        _scenario = exp_template.get("scenario")
        self.exp_topo = Experiment(_id, _name, _scenario)
        self.exp_topo.build()

    def run(self):
        self.exp_topo.start()
        self.exp_topo.wait_experiment(10)
        self.exp_topo.stop()


if __name__ == "__main__":
    inputs = {
        "vnf_id": "d2",
        "vnf_name": "sut",
        "vnf_version": 0.1,
        "vnf_image": "vnf-bench/suricata:0.1",
        "agent_1_id": "d1",
        "agent_1_image": "taas/beta:0.4",
        "agent_2_id": "d3",
        "agent_2_image": "taas/beta:0.4",
        "monitor_id": "d6",
        "network_id_1": 's1',
        "network_id_2": 's2',
    }

    p = Play()
    p.create_exp_topo("vnf-bd.yaml", inputs)
    # p.run()
