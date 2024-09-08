from __future__ import annotations
from flask import Flask, render_template, request
import main
import ClientAccount
import TellerAccount
import EtransferPayee
from datetime import datetime
import Payee

main.AccountInterface.tellerAcc.append(
    TellerAccount.TellerAccount("tahshins", "tahshin.shahriar", "abc")
)
main.AccountInterface.clientAcc.append(
    ClientAccount.ClientAccount(
        "slavass",
        "Slava",
        "slava123",
        "slava89@gmail.com",
        "7239739273",
        "hwkqehkwqehkehq",
    )
)
cli = main.AccountInterface.clientAcc[0]
cli.chequingAccount.deposit(100)
cli.addPayee(EtransferPayee.EtransferPayee("nasd", "asde", "email@am.com", "7361721"))
cli.openSavingsAccount()


application = Flask(__name__)
bank = main.AccountInterface()
teller = None
client = None


@application.route("/")
def home():
    return render_template("login.html")


# Login Page
@application.route("/login", methods=["POST"])
def login():
    acctypel = request.form.getlist("btnVal")
    acctype = acctypel[-1]

    if acctype == "bt":
        username = request.form["clusername"]
        password = request.form["clpasswd"]
        global teller
        teller = bank.login(username, password, "bt")
        if teller:
            return tellerInterface(teller)
        else:
            return "Input and Select all the fields properly"
    elif acctype == "cl":
        username = request.form["clusername"]
        password = request.form["clpasswd"]
        global client
        client = bank.login(username, password, "cl")
        if client:
            return clientInterface(client)
        else:
            return render_template(
                "login.html", errmsg="Input all the fields correctly"
            )


# Teller Interface
@application.route("/teler")
def tellerInterface(tellerObj):
    name = tellerObj.getUserName()
    idd = tellerObj.employeeID
    return render_template("tellerInterface.html", name=name, ID=idd)


@application.route("/thome")
def tellerHome():
    return tellerInterface(teller)


@application.route("/reg")
def register():
    return render_template("registration.html")


@application.route("/regp", methods=["POST"])
def reg():
    username = request.form["username"]
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    addr = request.form["addr"]

    clientp = teller.registerClient(username, name, email, phone, addr)

    if clientp:
        return render_template(
            "regsuccess.html",
            name=clientp.name_of_user,
            email=clientp.e_mail,
            passwd=clientp._password,
            phone=clientp.phone,
            accno=clientp._accountNumber,
            addr=clientp.address,
        )
    else:
        return "Reg failed!"


@application.route("/find")
def find():
    return render_template("find.html")


@application.route("/findp", methods=["POST"])
def findp():
    accno = request.form["accno"]
    clientp = teller.findClient(int(accno))

    if clientp:
        return render_template(
            "regsuccess.html",
            name=clientp.name,
            email=clientp.e_mail,
            phone=clientp.phone_no,
            accno=clientp._accountNumber,
            addr=clientp.address,
        )
    else:
        return "Client is not in the system!"


# Teller Ends


# Client Starts


@application.route("/client")
def clientInterface(clientObj):
    name = clientObj.username
    checkingsBalance = clientObj.chequingAccount.balance
    checkingsAccno = clientObj.chequingAccount.accountNumber
    if len(clientObj.savingsAccounts) > 0:
        savingsAcc = clientObj.savingsAccounts[0]
        savingsBalance = savingsAcc.balance
        savingsAccno = savingsAcc.accountNumber
    else:
        savingsBalance = "NIL"
        savingsAccno = "You don't have a Savings Account"

    if len(clientObj.creditAccounts) > 0:
        creditAcc = clientObj.creditAccounts[0]
        creditBalance = creditAcc.balance
        creditAccno = creditAcc.accountNumber
    else:
        creditBalance = "NIL"
        creditAccno = "You don't have a Credit Account"

    return render_template(
        "clientInt.html",
        name=name,
        cbalance=checkingsBalance,
        caccno=checkingsAccno,
        sbalance=savingsBalance,
        saccno=savingsAccno,
        ccbalance=creditBalance,
        ccaccno=creditAccno,
    )


# Home Page
@application.route("/chome")
def chome():
    return clientInterface(client)


# Apply for a Loan
@application.route("/applyLoan")
def loanapp():
    return render_template("applyLoan.html")


@application.route("/loanProccess", methods=["POST"])
def loanp():
    amount = request.form["amount"]
    loanType = request.form["type"]
    sDate = request.form["sdate"]
    startDate = datetime.strptime(sDate, "%Y-%m-%d")
    eDate = request.form["edate"]
    endDate = datetime.strptime(eDate, "%Y-%m-%d")
    loanSuccess = client.applyLoan(amount, loanType, startDate, endDate)
    if loanSuccess:
        return render_template(
            "applyLoanSuccess.html",
            balance=client.loans[-1].amount,
            loantype=client.loans[-1].type,
            sdate=client.loans[-1].startDate,
            edate=client.loans[-1].endDate,
        )
    else:
        return render_template(
            "applyLoan.html", errmsg="Input the fields appropriately"
        )


# Apply for a Credit Account
@application.route("/applyCredit")
def Credapp():
    return render_template("applyCredit.html")


@application.route("/creditProccess", methods=["POST"])
def Credp():
    credBalance = request.form["balance"]
    credSuccess = client.openCreditAccount(float(credBalance))
    if float(credBalance) < 500:
        return render_template("applyCredit.html", errmsg="Amount must be atleast 500")
    if credSuccess:
        return render_template(
            "applyCreditSuccess.html",
            accno=client.creditAccounts[0].accountNumber,
            cbalance=client.creditAccounts[0].balance,
            srate=client.creditAccounts[0].yearlyRate,
            cafee=client.creditAccounts[0].cashAdvanceFee,
        )
    else:
        return render_template(
            "applyCredit.html", errmsg="Input all the field correctly"
        )


# addPayee
@application.route("/addPayee")
def addpayee():
    return render_template("addPayee.html")


@application.route("/payeeProc", methods=["POST"])
def payeeProc():
    name = request.form["name"]
    desc = request.form["desc"]
    payee = Payee.Payee(name, desc)
    status = client.addPayee(payee)

    if status:
        return render_template(
            "addPayeesuccess.html",
            name=payee.name,
            id=payee.payeeID,
            desc=payee.description,
        )
    else:
        return "Error, couldn't add payee, try again"


# Open SavingsAccount
@application.route("/openSavings")
def Savingsapp():
    return render_template("openSavings.html")


@application.route("/savingsProc", methods=["POST"])
def savingsProc():
    savingsBalance = request.form["amount"]
    credSuccess = client.openSavingsAccount()
    if credSuccess:
        return render_template(
            "openSavingsSuccess.html",
            name=client.username,
            accno=client.savingsAccounts[0].accountNumber,
            amount=client.savingsAccounts[0].balance,
        )
    else:
        return render_template(
            "openSavings.html", errmsg="Input all the field correctly"
        )


# settings
@application.route("/settings")
def settings():
    return render_template("Settings.html")


# Change Details
@application.route("/details")
def details():
    return render_template("ChangeDet.html")


@application.route("/phoneProc", methods=["POST"])
def phonenoProc():
    phoneno = request.form["phoneno"]
    status = client.changePhone(phoneno)
    if status:
        return render_template("changeDetSuccess.html")
    else:
        return render_template("ChangeDet.html", errmsg="Input Phone No properly")


@application.route("/emailProc", methods=["POST"])
def Proc():
    email = request.form["email"]
    status = client.changePhone(email)
    if status:
        return render_template("changeDetSuccess.html")
    else:
        return render_template("ChangeDet.html", errmsg="Input Email properly")


@application.route("/addrProc", methods=["POST"])
def addrProc():
    addr = request.form["addr"]
    status = client.changePhone(addr)
    if status:
        return render_template("changeDetSuccess.html")
    else:
        return render_template("ChangeDet.html", errmsg="Input Address properly")


# Blockn Card
@application.route("/block")
def block():
    return render_template("BlockCard.html")


@application.route("/blockProc", methods=["POST"])
def blockProc():
    type = request.form["type"]
    if type == "Debit":
        client.chequingAccount.card.lockCard()
        client.savingsAccounts[0].card.lockCard()
        return render_template("BlockCardSuccess.html")
    elif type == "Credit":
        client.creditAccounts[0].card.lockCard()
        return render_template("BlockCardSuccess.html")
    else:
        return render_template("BlockCard.html", errmsg="Select Card Type")


# Delete account
@application.route("/delete")
def delete():
    return render_template("DeleteAcc.html")


# @application.route('/delproc')
# def delProc():
#     type = request.form['type']
#     passwd = request.form['passwd']
#     if client._password == passwd:
#         if type == "Savings":
#             client.


# Checkings Account
@application.route("/checkings")
def checkings():
    name = client.username
    checkingsBalance = client.chequingAccount.balance
    checkingsAccno = client.chequingAccount.accountNumber
    transactions = []
    for trnsac in client.chequingAccount.transactions:
        transacDict = {
            "sender": trnsac.sender,
            "receiver": trnsac.receiver,
            "amount": trnsac.amount,
            "type": trnsac.__class__.__name__,
        }
        transactions.append(transacDict)

    return render_template(
        "balanceAccount.html",
        name=name,
        caccno=checkingsAccno,
        cbalance=checkingsBalance,
        transactions=transactions,
    )


# SavingsAccount


@application.route("/savings")
def savings():
    name = client.username
    checkingsBalance = client.savingsAccounts[0].balance
    checkingsAccno = client.savingsAccounts[0].accountNumber
    transactions = []
    for trnsac in client.savingsAccounts[0].transactions:
        transacDict = {
            "sender": trnsac.sender,
            "receiver": trnsac.receiver,
            "amount": trnsac.amount,
            "type": trnsac.__class__.__name__,
        }
        transactions.append(transacDict)
    print(transactions)

    return render_template(
        "balanceAccount.html",
        name=name,
        caccno=checkingsAccno,
        cbalance=checkingsBalance,
        transactions=transactions,
    )


# CreditAccounts


@application.route("/credits")
def credits():
    name = client.username
    checkingsBalance = client.creditAccounts[0].balance
    checkingsAccno = client.creditAccounts[0].accountNumber
    transactions = []
    for trnsac in client.creditAccounts[0].transactions:
        transacDict = {
            "sender": trnsac.sender,
            "receiver": trnsac.receiver,
            "amount": trnsac.amount,
            "type": trnsac.__class__.__name__,
        }
        transactions.append(transacDict)

    return render_template(
        "balanceAccount.html",
        name=name,
        caccno=checkingsAccno,
        cbalance=checkingsBalance,
        transactions=transactions,
    )


# TransferFunds


@application.route("/transferFunds")
def transferFunds():
    return render_template("TransFunds.html")


@application.route("/transfundProc", methods=["POST"])
def transfundProc():
    fromAcc = request.form["fromAcc"]
    toAcc = request.form["toAcc"]
    amount = request.form["amount"]
    if len(client.savingsAccounts) == 0:
        return "You dont have a savings account"
    if fromAcc == "Savings" and toAcc == "Checkings":
        client.savingsAccounts[0].transferBetweenAccounts(
            float(amount), client.chequingAccount
        )
        return chome()
    elif fromAcc == "Checkings" and toAcc == "Savings":
        client.chequingAccount.transferBetweenAccounts(
            float(amount), client.savingsAccounts[0]
        )
        return chome()
    else:
        return "Input fields properly"


# AutoPayments


@application.route("/autoPayments")
def autoPayments():
    option_values = []
    for x in client.payees:
        option_values.append(x.payeeID)
    option_names = []
    for x in client.payees:
        option_names.append(x.name)
    application.jinja_env.globals.update(len=len)
    return render_template(
        "AutoPay.html", option_values=option_values, option_names=option_names
    )


@application.route("/autopaymentsProc", methods=["POST"])
def autopaymentsProcs():
    payeeID = request.form["payee"]
    amount = request.form["amount"]
    acctype = request.form["acctype"]

    for p in client.payees:
        if p.payeeID == int(payeeID):
            payee = p

    if acctype == "Savings":
        client.savingsAccounts[0].setupAutoPayment(payee, float(amount))
        return chome()
    elif acctype == "Checkings":
        client.chequingAccount.setupAutoPayment(payee, float(amount))
        return chome()
    else:
        return "error"


# Send Money


@application.route("/sendMoney")
def sendMoney():
    option_values = []
    option_names = []
    for x in client.payees:
        if isinstance(x, EtransferPayee.EtransferPayee):
            option_values.append(x.payeeID)
            option_names.append(x.name)
    application.jinja_env.globals.update(len=len)
    return render_template(
        "SendMoney.html", option_values=option_values, option_names=option_names
    )


@application.route("/sendmoneyProc", methods=["POST"])
def sendMoneyProc():
    id = request.form["payee"]
    acctype = request.form["acctype"]
    amount = request.form["amount"]
    payee = None
    for x in client.payees:
        if x.payeeID == int(id):
            payee = x
    if acctype == "Savings":
        if not client.savingsAccounts[0].sendEtransfer(
            float(amount), payee.email, payee.phone
        ):
            return "Not in payees"
        return chome()
    elif acctype == "Checkings":
        if not client.chequingAccount.sendEtransfer(
            float(amount), payee.email, payee.phone
        ):
            return "Not in payees"
        return chome()
    else:
        return "error"


# WireTransfer


@application.route("/wireTransfer")
def WireTransfer():
    return render_template("WireT.html")


@application.route("/wiretransferProc", methods=["POST"])
def wiretransferProc():
    details = request.form["details"]
    amount = request.form["amount"]
    acctype = request.form["acctype"]

    if acctype == "Savings":
        client.savingsAccounts[0].sendWireTransfer(float(amount), str(details))
        return chome()
    elif acctype == "Checkings":
        client.chequingAccount.sendWireTransfer(float(amount), str(details))
        return chome()
    else:
        return "error"


if __name__ == "__main__":
    application.run()
