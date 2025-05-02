#!/usr/bin/env python3
import os
import json

import aws_cdk as cdk

from bin.wgu_capstone_stack import WguCapstoneStack


app = cdk.App()
WguCapstoneStack(app, "WguCapstoneStack")

app.synth()
