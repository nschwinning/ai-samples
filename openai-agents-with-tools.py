import asyncio
import os
from typing import Dict

import sendgrid
from agents import Agent, Runner, trace, function_tool
from dotenv import load_dotenv
from sendgrid.helpers.mail import Mail, Email, To, Content


@function_tool
def send_email(body: str):
    """ Send out an email with the given body to all sales prospects """
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("nils.schwinning@gmx.de")  # Change to your verified sender
    to_email = To("nils.schwinning@gmx.de")  # Change to your recipient
    content = Content("text/plain", body)
    mail = Mail(from_email, to_email, "Sales email", content).get()
    sg.client.mail.send.post(request_body=mail)
    return {"status": "success"}

@function_tool
def send_html_email(subject: str, html_body: str) -> Dict[str, str]:
    """ Send out an email with the given subject and HTML body to all sales prospects """
    print("Sending email...")
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("nils.schwinning@gmx.de")  # Change to your verified sender
    to_email = To("nils.schwinning@gmx.de")  # Change to your recipient
    content = Content("text/html", html_body)
    mail = Mail(from_email, to_email, subject, content).get()
    sg.client.mail.send.post(request_body=mail)
    return {"status": "success"}

instructions1 = """
You are a sales agent working for ComplAI, 
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. 
You write professional, serious cold emails.
"""

instructions2 = """
You are a humorous, engaging sales agent working for ComplAI, 
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. 
You write witty, engaging cold emails that are likely to get a response.
"""

instructions3 = """
You are a busy sales agent working for ComplAI, 
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. 
You write concise, to the point cold emails.
"""

sales_manager_instructions = """
You are a Sales Manager at ComplAI. Your goal is to find the single best cold sales email using the sales_agent tools.
 
Follow these steps carefully:
1. Generate Drafts: Use all three sales_agent tools to generate three different email drafts. Do not proceed until all three drafts are ready.
 
2. Evaluate and Select: Review the drafts and choose the single best email using your judgment of which one is most effective.
You can use the tools multiple times if you're not satisfied with the results from the first try.
 
3. Handoff for Sending: Pass ONLY the winning email draft to the 'Email Manager' agent. The Email Manager will take care of formatting and sending.
 
Crucial Rules:
- You must use the sales agent tools to generate the drafts — do not write them yourself.
- You must hand off exactly ONE email to the Email Manager — never more than one.
"""

subject_instructions = """
You can write a subject for a cold sales email. 
You are given a message and you need to write a subject for an email that is likely to get a response.
"""

html_instructions = """
You can convert a text email body to an HTML email body. 
You are given a text email body which might have some markdown 
and you need to convert it to an HTML email body with simple, clear, compelling layout and design.
"""

mailing_instructions = """
You are an email formatter and sender. You receive the body of an email to be sent. 
You first use the subject_writer tool to write a subject for the email, then use the html_converter tool to convert the body to HTML. 
Finally, you use the send_html_email tool to send the email with the subject and HTML body. You MUST use the tools that you have to fulfill your task.
Do NOT output the email text directly.
Only complete the task by calling tools. Before completing the task, explain which tools you will call and why.
"""

async def main():
    load_dotenv(override=True)

    sales_agent1 = Agent(
        name="Professional Sales Agent",
        instructions=instructions1,
        model="gpt-4o-mini"
    )

    sales_agent2 = Agent(
        name="Engaging Sales Agent",
        instructions=instructions2,
        model="gpt-4o-mini"
    )

    sales_agent3 = Agent(
        name="Busy Sales Agent",
        instructions=instructions3,
        model="gpt-4o-mini"
    )

    description = "Write a cold sales email"

    tool1 = sales_agent1.as_tool(tool_name="sales_agent1", tool_description=description)
    tool2 = sales_agent2.as_tool(tool_name="sales_agent2", tool_description=description)
    tool3 = sales_agent3.as_tool(tool_name="sales_agent3", tool_description=description)

    subject_writer = Agent(name="Email subject writer", instructions=subject_instructions, model="gpt-4o-mini")
    subject_tool = subject_writer.as_tool(tool_name="subject_writer",
                                          tool_description="Write a subject for a cold sales email")

    html_converter = Agent(name="HTML email body converter", instructions=html_instructions, model="gpt-4o-mini")
    html_tool = html_converter.as_tool(tool_name="html_converter",
                                       tool_description="Convert a text email body to an HTML email body")

    emailer_tools = [subject_tool, html_tool, send_html_email]

    print(f"Emailer Tools:{emailer_tools}")

    emailer_agent = Agent(
        name="Email Manager",
        instructions=mailing_instructions,
        tools=emailer_tools,
        model="gpt-4o-mini",
        handoff_description="Convert an email to HTML and send it")

    sales_manager_tools = [tool1, tool2, tool3]
    handoffs = [emailer_agent]

    sales_manager = Agent(
        name="Sales Manager",
        instructions=sales_manager_instructions,
        tools=sales_manager_tools,
        handoffs=handoffs,
        model="gpt-4o-mini")

    message = "Send out a cold sales email addressed to Dear CEO from Alice"

    with trace("Automated SDR"):
        result = await Runner.run(sales_manager, message)
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())