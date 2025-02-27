Browser Use home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/browseruse-0aece648/logo/light.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/browseruse-0aece648/logo/dark.svg)
Search or ask...
Ctrl K
Search...
Navigation
Customize
Connect to your Browser
DocumentationCloud API
##### Get Started
  * Introduction
  * Quickstart


##### Customize
  * Supported Models
  * Agent Settings
  * Browser Settings
  * Connect to your Browser
  * Output Format
  * System Prompt
  * Sensitive Data
  * Custom Functions


##### Development
  * Local Setup
  * Telemetry
  * Observability
  * Roadmap


## 
​
Overview
You can connect the agent to your real Chrome browser instance, allowing it to access your existing browser profile with all your logged-in accounts and settings. This is particularly useful when you want the agent to interact with services where you’re already authenticated.
First make sure to close all running Chrome instances.
## 
​
Basic Configuration
To connect to your real Chrome browser, you’ll need to specify the path to your Chrome executable when creating the Browser instance:
Copy
```
from browser_use import Agent, Browser, BrowserConfig
from langchain_openai import ChatOpenAI
import asyncio
# Configure the browser to connect to your Chrome instance
browser = Browser(
  config=BrowserConfig(
    # Specify the path to your Chrome executable
    chrome_instance_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', # macOS path
    # For Windows, typically: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    # For Linux, typically: '/usr/bin/google-chrome'
  )
)
# Create the agent with your configured browser
agent = Agent(
  task="Your task here",
  llm=ChatOpenAI(model='gpt-4o'),
  browser=browser,
)
async def main():
  await agent.run()
  input('Press Enter to close the browser...')
  await browser.close()
if __name__ == '__main__':
  asyncio.run(main())

```

When using your real browser, the agent will have access to all your logged-in sessions. Make sure to review the task you’re giving to the agent and ensure it aligns with your security requirements.
Was this page helpful?
YesNo
Browser SettingsOutput Format
On this page
  * Overview
  * Basic Configuration


