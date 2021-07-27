from django.shortcuts import render, redirect, reverse
from web3 import Web3, WebsocketProvider, HTTPProvider
from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse, HttpResponse
from time import sleep
from django.contrib import messages
from datetime import datetime
import json

# Create your views here.
w3 = Web3(HTTPProvider("HTTP://127.0.0.1:7545"))
acc = {
  'sender': '',
  'pk': '',
  'name': '',
}
contract = {
    'owner': '',
    'address': "0x632442372726AD0A21Cb4C10862F48D219dA1A61",
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
      "gas": 589400,
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
      "gas": 852177,
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
      "gas": 1358063,
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
      "gas": 763174314,
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
      "gas": 446888,
      "inputs": [],
      "name": "get_list_of_company_acc",
      "outputs": [
        {
          "name": "",
          "type": "address[500]"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "gas": 2115148,
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
      "gas": 28022777,
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
      "gas": 582210,
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
      "gas": 583430,
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
      "gas": 1388,
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
contract['owner'] = pid.functions.contract_owner().call()

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

def get_company_name_list(_sender):
    w3.eth.defaultAccount = _sender
    tmp = pid.functions.get_list_of_company_acc().call()
    new_list = []
    for key, val in enumerate(tmp):
        if '0x000' in val:
            return new_list
        new_list.append(get_company_account_name(val))
    return new_list

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

def register_product(_pk, _name, _category, _release_year, _price, _country, _description, _serial_list, _sender, _key):
    w3.eth.defaultAccount = _sender
    nonce = w3.eth.getTransactionCount(_sender)
    txn = pid.functions.register_product(_pk, _name, _category, _release_year, _price, _country, _description, _serial_list).buildTransaction({
        'gas': 3000000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'nonce': nonce
    })
    result = run_transaction(txn, _key)
    return result

def get_list_of_products(_sender):
    w3.eth.defaultAccount = _sender
    tmp = pid.functions.get_list_of_products(generate_arr([], b'0', 1000)).call()
    new_list = []
    for key, val in enumerate(tmp):
        if str(clean_bytes(val)) != '0':
            new_list.append(clean_bytes(val))
    return new_list

def get_first_product(_sender):
    w3.eth.defaultAccount = _sender
    return pid.functions.get_first_product().call()

# Return the last product of the company acc
def get_last_product(_sender):
    w3.eth.defaultAccount = _sender
    return pid.functions.get_last_product().call()

def get_product_prop(_pk, _sender):
    w3.eth.defaultAccount = _sender
    tmp = pid.functions.get_product_prop(_pk).call()
    tmp[5] = [val for val in tmp[5] if val != 0]
    data = {
        'name': clean_bytes(tmp[0][0]),
        'category': clean_bytes(tmp[0][1]),
        'release_year': tmp[1],
        'price': tmp[2],
        'country': clean_bytes(tmp[3]),
        'description': tmp[4],
        'serial_lists': tmp[5]
    } 
    return data

def update_product(_target_pk, _name, _category, _price, _description, _sender, _key):
    w3.eth.defaultAccount = _sender
    nonce = w3.eth.getTransactionCount(_sender)
    txn = pid.functions.update_product(_target_pk, _name, _category, _price,_description).buildTransaction({
        'gas': 3000000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'nonce': nonce
    })
    signed_txn = w3.eth.account.signTransaction(txn, private_key=_key)
    signed_txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    return w3.eth.waitForTransactionReceipt(signed_txn_hash)

def isLogin(request):
  if request.session.get('acc', False):
    return request.session['acc']
  return False

class Index(generic.TemplateView):
  template_name = 'pidapp/index.html'

class Dashboard(generic.TemplateView):
  template_name = 'pidapp/dashboard.html'

  def get(self, *args, **kwargs):
    acc = isLogin(self.request)
    if not acc:
      return redirect(reverse('pidapp:login'))
    print("You're already login", acc)
    list_products, first_prod, last_prod = '', '', ''
    context = dict()
    try:
      list_products = get_list_of_products(acc['pub'])
      first_prod = get_first_product(acc['pub'])
      last_prod = get_last_product(acc['pub'])
      context = {'products': list_products, 'first_prod': first_prod, 'last_prod': clean_bytes(last_prod)}
      list_products.pop()
      context['num_products'] = len(list_products)
      print("getting anything yet?", context)
      return render(self.request, self.template_name, context)
    except:
      print("Error")
    return render(self.request, self.template_name, context)

class Login(generic.TemplateView):
  template_name = 'auth/login.html'

  def post(self, *args, **kwargs):
    if self.request.is_ajax and self.request.method == "POST":
      pub, pw = w3.toChecksumAddress(self.request.POST.get("username", None)), self.request.POST.get("password", None)
      pk = get_secret_key(pub, pw.encode())
      name = get_company_account_name(pub)
      if (len(pk) and len(pub)):
        context = {'pub': pub, 'name': name}
        print("Reaching here?", context)
        self.request.session['acc'] = {
          'pub': pub,
          'name': name,
          'login': True,
          'pk': pk
        }
        messages.info(self.request, "Login completed!")
        return redirect(reverse('pidapp:dashboard'))
      else:
        messages.warning(self.request, "Login failed, please try again")
        return JsonResponse({"status": False}, status=400)

class Register(generic.TemplateView):
  template_name = 'auth/register.html'

  def get(self, *args, **kwargs):
    company_names = get_company_name_list(contract['owner'])
    print(company_names)
    return render(self.request, self.template_name, {'used': company_names})
 
  def post(self, *args, **kwargs):
    if self.request.is_ajax and self.request.method == "POST":
      name, pub, pk, pw = self.request.POST.get('company-name', None), w3.toChecksumAddress(self.request.POST.get("pub", None)), self.request.POST.get("pk", None), self.request.POST.get("pw", None) 
      nonce = w3.eth.getTransactionCount(pub)
      name, pw = name.encode(), pw.encode()
      try:
        result = register_company_account(pub, name, pk, pw)
        print(result)
        return redirect(reverse('pidapp:login'))
      except ValueError:
        messages.info(self.request, "You already registered")
      messages.warning(self.request, "Sign up failed, you can contact the admin")
      return JsonResponse({"status": False}, status=400)
    return JsonResponse({}, status=400)

def logout(request):
  try:
    del request.session['acc']
  except KeyError:
    pass
  messages.info(request, "Sign out completed")
  return redirect(reverse('pidapp:login'))



def validate_product_serial(_pk, _serial_key, _sender): 
    tmp = get_product_prop(_pk, _sender)
    return _serial_key in tmp['serial_lists']

class RegisterProduct(generic.TemplateView):
  template_name = 'pidapp/register_product.html'

  def get(self, *args, **kwargs):
    acc = isLogin(self.request)
    if not acc:
      return redirect(reverse('pidapp:login'))
    return render(self.request, self.template_name, dict())

  def post(self, *args, **kwargs):
    if self.request.is_ajax and self.request.method == "POST":
      acc = isLogin(self.request)
      if not acc:
          return redirect(reverse('pidapp:login'))
      form = {'p-name': '', 'p-category': '', 'p-year': '', 'p-country': '', 'p-price': '', 'description':'', 'serial-lists': ''}
      for key, val in form.items():
        form[key] = self.request.POST.get(key, None)
      form['serial-lists'] = json.loads(form['serial-lists'])
      print("Form", form)
      temp = form['serial-lists']
      print("TEMP", temp)
      if len(temp) != len(set(temp)):
        messages.info(self.request, "Serial List must be unique")
        return JsonResponse({'error': "Serial key must be unique" }, status=400)
      pk = generate_pk(form['p-name'])
      temp = generate_arr(temp, 0, 10)
      print("After Temp", form)
      result = register_product(pk.encode(), form['p-name'].encode(), form['p-category'].encode(), int(form['p-year']), int(form['p-price']), form['p-country'].encode(), form['description'], temp, acc['pub'], acc['pk'])
      return JsonResponse({'new': "You have registered product successfully"}, status=200)
    return JsonResponse({'error': 'error'}, status=400)

class ViewProduct(generic.TemplateView):
  template_name = 'pidapp/view_product_unit.html'

  def get(self, *args, **kwargs):
    acc = isLogin(self.request)
    if not acc:
      return redirect(reverse('pidapp:login'))
    prod_pk = self.kwargs['prod_pk']
    context = get_product_prop(prod_pk.encode(), acc['pub'])
    context['prod_pk'] = prod_pk
    return render(self.request, self.template_name, context)

class EditProduct(generic.TemplateView):
  template_name = 'pidapp/edit_product.html'

  def get(self, *args, **kwargs):
    acc = isLogin(self.request)
    if not acc:
      return redirect(reverse('pidapp:login'))
    prod_pk = self.kwargs['prod_pk']
    context = get_product_prop(prod_pk.encode(), acc['pub'])
    context['prod_pk'] = prod_pk 
    return render(self.request, self.template_name, context)

  def post(self, *args, **kwargs):
    if self.request.is_ajax and self.request.method == "POST":
      acc = isLogin(self.request)
      if not acc:
          return redirect(reverse('pidapp:login'))
      print(acc)
      prod_pk = self.request.POST.get('prod_pk')
      form = {'p-name': '', 'p-category': '', 'p-price': '', 'description':''}
      for key, val in form.items():
        form[key] = self.request.POST.get(key, None)
      messages.info(self.request, "You have registered a product")
      result = update_product(prod_pk.encode(), form['p-name'].encode(), form['p-category'].encode(), int(form['p-price']), form['description'], acc['pub'], acc['pk'])
      return JsonResponse({'new': "Update successfully"}, status=200)
    return JsonResponse({}, status=400)

def get_company_pk_list(_sender):
    w3.eth.defaultAccount = _sender
    tmp = pid.functions.get_list_of_company_acc().call()
    new_list = []
    for key, val in enumerate(tmp):
        if '0x000' in val:
            return new_list
        new_list.append(val)
    return new_list

def validate_product(request):
  prod_pk, serial_key = request.POST['prod_pk'], request.POST['serial_key']
  prod_pk, serial_key = prod_pk.encode(), int(serial_key)
  print(prod_pk, serial_key, contract['owner'])
  all = get_company_pk_list(contract['owner'])
  isValid = False
  for company in all:
    isValid = validate_product_serial(prod_pk, serial_key, company)
    if isValid:
      break
  print(isValid)
  return JsonResponse({'result': isValid}, status=200);


