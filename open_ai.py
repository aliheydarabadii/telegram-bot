import time

def send_message(message,thread,client,my_assistant):
  message = client.beta.threads.messages.create(
      thread_id=thread.id,
      role="user",
      content=message
  )
  run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=my_assistant.id,
    instructions="Please recomend him movie."
  )
  while True:
    run = client.beta.threads.runs.retrieve(
      thread_id=thread.id,
      run_id=run.id
    )
    if run.status == 'completed':
      break
    time.sleep(3)
    print(run.status)

  messages = client.beta.threads.messages.list(
    thread_id=thread.id
  )
  return messages.data[0].content[0].text.value