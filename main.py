import datetime
import looker_sdk
from looker_sdk import models40 #using Looker 4.0
from pprint import pprint




def hello_world(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()

    print("This is the request message along with HTTP tigger ",request_json)

    if request.args and 'expiry_duration' in request.args:
        expiry_duration = request.args.get('expiry_duration')
    elif request_json and 'expiry_duration' in request_json:
        expiry_duration = request_json['expiry_duration']
    else:
        expiry_duration = 365

    print("expity_duration is ",expiry_duration)

    #Initialize Looker SDK
    sdk = looker_sdk.init40()
    all_schedule_plans = sdk.all_scheduled_plans(all_users=True)

    # Holds all the plans
    plans={}

    today = datetime.date.today()

    for plan in all_schedule_plans:
        print("Processing the schedule plan : ",plan['id'], "it has ",len(plan['scheduled_plan_destination'])," destinations")
        
        # Plan expiry date based user input 'expiry_duration'
        expr_date = (plan['created_at']+datetime.timedelta(days=expiry_duration)).date()
        
        if today >= expr_date:
            try:
                response = sdk.delete_scheduled_plan(scheduled_plan_id=plan['id'])
            except:
                print("Something went woring in delete_scheduled_plan")
            continue

        plan_dest_body=[]
        for plan_destination in plan['scheduled_plan_destination']:
            body = dict(plan_destination)
            #body['message']=  "This will expire in about "+ expr_date.strftime("%m/%d/%Y")
            body['message']=  "Custom Message..."
            plan_dest_body.append(models40.ScheduledPlanDestination(**body))
    
        pprint("Updating the the plan destination property as follows\n", plan_dest_body)
        try:
            response = sdk.update_scheduled_plan(scheduled_plan_id=plan['id'],body = models40.WriteScheduledPlan(
                scheduled_plan_destination=plan_dest_body
                ))

        except:
            print("Something woring with update_scheduled_plan")

    return "Sucessful"
