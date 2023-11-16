import mqttapi as mqtt
import datetime
from pyHS100 import SmartStrip

class TplinkPowerStrip(mqtt.Mqtt):

  def initialize(self):
    self.log("Starting TplinkPowerStrip")
    self.run_every(self.check_power, "now", 10)
    self.plug = SmartStrip(self.args["host"])

  def check_power(self, kwargs):
    base = self.args["topic"]
    #self.log("check_power " + self.args["host"])
    for port in range(6):
      topic = base + str(port)
      try:
          curr = self.plug.current_consumption(index=port)
      except:
          return;

      power = round(curr, 1)
      #self.log("mqtt " + topic + " => " + str(power))
      self.mqtt_publish(topic, power)
