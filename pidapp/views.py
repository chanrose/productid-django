from django.shortcuts import render, redirect, reverse
from web3 import Web3, WebsocketProvider, HTTPProvider
from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse, HttpResponse
from time import sleep
from django.contrib import messages

# Create your views here.
w3 = Web3(HTTPProvider("HTTP://127.0.0.1:7545"))
acc = {
  'sender': '',
  'pk': '',
  'name': '',
}
contract = {
    'address': "0x560a99A9E230371E7177504169db120842c48800",
    'abi': '''[
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "name": "_pub_key",
          "type": "address"
        },
        {
          "indexed": false,
          "name": "_name",
          "type": "bytes32"
        },
        {
          "indexed": false,
          "name": "_timestamp",
          "type": "uint256"
        }
      ],
      "name": "Account_Creation",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "name": "_pub_key",
          "type": "address"
        },
        {
          "indexed": false,
          "name": "_pk",
          "type": "bytes32"
        },
        {
          "indexed": false,
          "name": "_name",
          "type": "bytes32"
        },
        {
          "indexed": false,
          "name": "_timestamp",
          "type": "uint256"
        }
      ],
      "name": "Product_Registration_Update",
      "type": "event"
    },
    {
      "inputs": [],
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "gas": 1169400,
      "inputs": [
        {
          "name": "_password",
          "type": "bytes32"
        }
      ],
      "name": "get_secret_key",
      "outputs": [
        {
          "name": "",
          "type": "string"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "gas": 1432177,
      "inputs": [
        {
          "name": "_name",
          "type": "bytes32"
        },
        {
          "name": "_secret_key",
          "type": "string"
        },
        {
          "name": "_password",
          "type": "bytes32"
        }
      ],
      "name": "register_company_account",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "gas": 1331,
      "inputs": [],
      "name": "get_company_account_name",
      "outputs": [
        {
          "name": "",
          "type": "bytes32"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "gas": 1938063,
      "inputs": [
        {
          "name": "_pk",
          "type": "bytes32"
        },
        {
          "name": "_name",
          "type": "bytes32"
        },
        {
          "name": "_category",
          "type": "bytes32"
        },
        {
          "name": "_release_year",
          "type": "uint256"
        },
        {
          "name": "_price",
          "type": "uint256"
        },
        {
          "name": "_country",
          "type": "bytes32"
        },
        {
          "name": "_description",
          "type": "string"
        },
        {
          "name": "_serial_lists",
          "type": "uint256[10]"
        }
      ],
      "name": "register_product",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "gas": 763754314,
      "inputs": [
        {
          "name": "_target_product_pk",
          "type": "bytes32"
        },
        {
          "name": "_name",
          "type": "bytes32"
        },
        {
          "name": "_category",
          "type": "bytes32"
        },
        {
          "name": "_price",
          "type": "uint256"
        },
        {
          "name": "_description",
          "type": "string"
        }
      ],
      "name": "update_product",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "gas": 2695118,
      "inputs": [
        {
          "name": "_arr",
          "type": "bytes32[1000]"
        }
      ],
      "name": "get_list_of_products",
      "outputs": [
        {
          "name": "",
          "type": "bytes32[1000]"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "gas": 28022747,
      "inputs": [
        {
          "name": "_pk",
          "type": "bytes32"
        }
      ],
      "name": "get_product_prop",
      "outputs": [
        {
          "name": "",
          "type": "bytes32[2]"
        },
        {
          "name": "",
          "type": "uint256"
        },
        {
          "name": "",
          "type": "uint256"
        },
        {
          "name": "",
          "type": "bytes32"
        },
        {
          "name": "",
          "type": "string"
        },
        {
          "name": "",
          "type": "uint256[10]"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "gas": 1162180,
      "inputs": [],
      "name": "get_first_product",
      "outputs": [
        {
          "name": "",
          "type": "bytes32"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "gas": 1163400,
      "inputs": [],
      "name": "get_last_product",
      "outputs": [
        {
          "name": "",
          "type": "bytes32"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "gas": 1358,
      "inputs": [],
      "name": "contract_owner",
      "outputs": [
        {
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    }
  ]'''
}

pid = w3.eth.contract(address=contract['address'], abi=contract['abi'])

# Internal Function
# Generating custom array 
def generate_arr(arr, placeholder, size):
    while size > len(arr):
        arr.append(placeholder)
    return arr

# Generating unique product name with timestamp as based
def generate_pk(_product_name):
    now = str(datetime.now().timestamp())
    return(_product_name + now)

# Clean Bytes \x00 
def clean_bytes(_input):
    return _input.decode().rstrip('\x00')


def get_secret_key(_sender, _pw):
    w3.eth.defaultAccount = _sender
    return pid.functions.get_secret_key(_pw).call()

def get_company_account_name(_sender):
    w3.eth.defaultAccount = _sender
    return clean_bytes(pid.functions.get_company_account_name().call())

def register_company_account(_sender, _name, _sec, _pw):
    nonce = w3.eth.getTransactionCount(_sender)
    txn = pid.functions.register_company_account(_name, _sec, _pw).buildTransaction({
        'gas': 2000000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'nonce': nonce
    })
    result = run_transaction(txn, _sec)
    return result

def run_transaction(tx, pk):
  signed_tx = w3.eth.account.signTransaction(tx,pk)
  tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
  tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
  count = 1
  while tx_receipt is None and (count < 30):
    sleep(10)
    result = tx_receipt
    tx_receipt = w3.eth.getTransactionReceipt(result)
    count = count + 1
  print(tx_receipt)
  return tx_receipt

def isLogin():
  if len(acc['pk']) and len(acc['sender']):
    return True
  return False

class Index(generic.TemplateView):
  template_name = 'pidapp/index.html'

class Dashboard(generic.TemplateView):
  template_name = 'pidapp/dashboard.html'

  def get(self, *args, **kwargs):
    if isLogin():
      context = {
        'name': acc['name']
      }
      print("you're login", context)
    else:
      return redirect(reverse('pidapp:login'))
    return render(self.request, self.template_name, dict())

class Login(generic.TemplateView):
  template_name = 'auth/login.html'

  def post(self, *args, **kwargs):
    if self.request.is_ajax and self.request.method == "POST":
      pub, pw = w3.toChecksumAddress(self.request.POST.get("username", None)), self.request.POST.get("password", None)
      pk = get_secret_key(pub, pw.encode())
      name = get_company_account_name(pub)
      if (len(pk) and len(pub)):
        acc['sender'], acc['pk'], acc['name'] = pub, pk, name
        context = {'pub': pub, 'name': name}
        print("Reaching here?", context)
        messages.info(self.request, "Login completed!")
        return redirect(reverse('pidapp:dashboard'))
      else:
        messages.warning(self.request, "Login failed, please try again")
        return JsonResponse({"status": False}, status=400)

class Register(generic.TemplateView):
  template_name = 'auth/register.html'

  def post(self, *args, **kwargs):
    if self.request.is_ajax and self.request.method == "POST":
      name, pub, pk, pw = self.request.POST.get('company-name', None), w3.toChecksumAddress(self.request.POST.get("pub", None)), self.request.POST.get("pk", None), self.request.POST.get("pw", None) 
      nonce = w3.eth.getTransactionCount(pub)
      name, pw = name.encode(), pw.encode()
      try:
        result = register_company_account(pub, name, pk, pw)
        print(result)
        return JsonResponse({"status":True}, status=200)
      except ValueError:
        messages.info(self.request, "You already registered")
      messages.warning(self.request, "Sign up failed, you can contact the admin")
      return JsonResponse({"status": False}, status=400)
    return JsonResponse({}, status=400)

def logout(request):
  acc['sender'], acc['pk'], acc['name'] = '', '', ''
  messages.info(request, "Sign out completed")
  return redirect(reverse('pidapp:login'))



