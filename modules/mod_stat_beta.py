from libs.module import *
from libs.correl import *


class mod_stat_beta(CANModule):
    name = "Service discovery and statistic"

    help = """ """
    
    def do_init(self, params):
        self.all_frames = []
        self._cmdList['p'] = ["Print data", 0, "", self.do_print, True]

    def do_print(self):

        align = ForcedSampler(1, same)
        subnet = Subnet(lambda stream: Separator(SeparatedMessage.builder))

        normalize = Subnet(lambda stream: Normalizer(10, FloatMessage.simple))

        conv = ForcedSampler(2, FloatMessage.conv)
        integrate = Integrator(100, FloatMessage.simple)

        #for msg in integrate(conv(normalize(subnet(align(dump))))):
        #    if float(msg) > 1:
        #        print(msg, float(msg))

    # Effect (could be fuzz operation, sniff, filter or whatever)
    def do_effect(self, can_msg, args):
        if can_msg.CANData:
            self.all_frames.append(can_msg) # ADD NEW CAN MESSAGE
        return can_msg
