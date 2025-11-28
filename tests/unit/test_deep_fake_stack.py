import aws_cdk as core
import aws_cdk.assertions as assertions

from deep_fake.deep_fake_stack import DeepFakeStack

# example tests. To run these tests, uncomment this file along with the example
# resource in deep_fake/deep_fake_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = DeepFakeStack(app, "deep-fake")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
