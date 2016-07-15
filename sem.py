import sys,os, shutil, json

def users(commands,options):
    # going to do the rest in control-flow since I'm lazy
    if commands[0] == "delete":
        delAll = False
        for i in options:
            if i == "all":
                delAll = True
        if delAll == True:
            shutil.rmtree("userData/userFiles")
            os.makedirs("userData/userFiles")
            writer = open("userData/IpList.json",'w')
            writer.write("{}")
            writer.close()
        else:
            r = open("userData/IpList.json",'r')
            jsonDocs = json.loads(r.read())
            r.close()
            shutil.rmtree("userData/userFiles/" + commands[1])
            jsonDocs.pop(commands[1].replace("-","."))
            jsonStr = json.dumps(jsonDocs, indent=4, sort_keys=True)
            writer = open("userData/IpList.json",'w')
            writer.write(jsonStr)
            writer.close()
            print("Succesfully deleted all data for ip: " + commands[1].replace("-","."))
    pass

def main():
    args = sys.argv[1:]
    options = []
    commands = []
    for i in args:
        if i[0].find("-") > -1:
            options.append(i.replace("-",""))
        else:
            commands.append(i)
    base_commands = ["users"]
    for i in base_commands:
        for j in commands:
            if j == i:
                commands.remove(i)
                eval(i + "(" + str(commands) + "," + str(options) + ")")

if __name__ == '__main__':
    main()
    