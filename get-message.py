import boto3
from botocore.exceptions import ClientError
import requests
import json

# Set up your SQS queue URL and boto3 client
url = "https://sqs.us-east-1.amazonaws.com/440848399208/zhr8wex"
sqs = boto3.client('sqs')

def delete_message(handle):
    try:
        # Delete message from SQS queue
        sqs.delete_message(
            QueueUrl=url,
            ReceiptHandle=handle
        )
        print("Message deleted")
    except ClientError as e:
        print(e.response['Error']['Message'])



#need to do x10 times, without running separatly 10 times
def get_message():

    #fancy method of initalizing arrays, learnt it while I was grinding LeetCode
    myWords = [""] * 10

    #order doesn't matter, just append handles to this array
    delete_arr = []


    count = 0
    while count < 10:
        try:
            # Receive message from SQS queue. Each message has two MessageAttributes: order and word
            # You want to extract these two attributes to reassemble the message
            response = sqs.receive_message(
                QueueUrl=url,
                AttributeNames=[
                    'All'
                ],
                MaxNumberOfMessages=1,
                MessageAttributeNames=[
                    'All'
                ]
            )
            # Check if there is a message in the queue or not
            if "Messages" in response:
                # extract the two message attributes you want to use as variables
                # extract the handle for deletion later
                order = response['Messages'][0]['MessageAttributes']['order']['StringValue']
                word = response['Messages'][0]['MessageAttributes']['word']['StringValue']
                handle = response['Messages'][0]['ReceiptHandle']

                # Print the message attributes - this is what you want to work with to reassemble the message
                # print(f"Order: {order}")
                # print(f"Word: {word}")

                #assign words in order, use int() to index array
                myWords[int(order)] = word
                delete_arr.append(handle)
                count += 1

            # If there is no message in the queue, print a message and exit    
            #else:
                #print("No message in the queue")
                #exit(1)
                
        # Handle any errors that may occur connecting to SQS
        except ClientError as e:
            print(e.response['Error']['Message'])

            #break the while loop
            break

    #accumulate words from array into string
    ret = ""
    for n in range(len(myWords)):
        #add word to return var
        ret += myWords[n]

        #if not last word, add space after
        if n != len(myWords) - 1:
            ret += " "
    
    #display string
    print(ret)

    #Loop through delete_arr
    for h in delete_arr:
        #call delete_message on handle
        delete_message(h)

# Trigger the function
if __name__ == "__main__":
    get_message()