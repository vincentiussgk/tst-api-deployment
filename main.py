# Read Data from JSON
import json

with open("data/pembeli.json", "r+") as read_file:
    pembeliData = json.load(read_file)

with open("data/penjualan.json", "r+") as read_file:
    penjualanData = json.load(read_file)

with open("data/production.json", "r+") as read_file:
    productionData = json.load(read_file)

with open("data/supply.json", "r+") as read_file:
    supplyData = json.load(read_file)

with open("data/users.json", "r+") as read_file:
    usersData = json.load(read_file)

from auth.auth_handler import signJWT
from auth.helpers import check_user, get_password_hash, user_exists, verify_password
from auth.auth_bearer import JWTBearer
from fastapi import FastAPI, HTTPException, Depends, Body

app = FastAPI()

@app.post('/users')
def create_user(username: str, password: str):
    with open("data/users.json", "r+") as data_file:
        userData = json.load(data_file)
    creds = {
        "username": username, 
        "password": get_password_hash(password)
    }
    if not (user_exists(userData, username)):
        userData.append(creds)
        with open ("data/users.json", "w") as user_file:       
            json.dump(userData, user_file, indent=4)
        return signJWT(username)
    else:
        raise HTTPException(status_code=405, detail=f'User already exists.')

# Login
@app.post('/users/login')
def login (username: str, password: str):
    with open("data/users.json", "r+") as data_file:
        userData = json.load(data_file)
    creds = {
        "username": username, 
        "password": password
    }
    checkUser = check_user(userData, creds)
    print(check_user)
    if (checkUser == 200):
        return signJWT(username)
    elif (checkUser == 403):
        raise HTTPException(status_code=403, detail=f'Wrong password.')
    else:
        raise HTTPException(status_code=404, detail=f'User not found.')

@app.get("/")
async def landing():
    return {
        "message": "Server Successfully runnning"
    }

# API bagian Supply
@app.get("/supply", dependencies=[Depends(JWTBearer())])
async def get_all_supplies():
    with open("data/supply.json", "r+") as read_file:
        data = json.load(read_file)
    if len(data) < 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Supplies were found")
    return data

@app.get("/supply/{supply_id}", dependencies=[Depends(JWTBearer())])
async def get_a_supply(supply_id):
    with open("data/supply.json", "r+") as read_file:
        data = json.load(read_file)
    for menu_item in data:
        if menu_item['id'] == supply_id:
            return menu_item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supply Not Found")

@app.post("/supply", dependencies=[Depends(JWTBearer())])
async def add_supply(
        nama_produk: str,
        jumlah: int,
        deskripsi: str,
        jenis: str,
        status: str
    ):
    with open("data/supply.json", "r+") as read_file:
        data = json.load(read_file)
    newItemId = data[-1]["id"]+1 if len(data) > 0 else 1
    data.append({
        "id": newItemId,
        "nama_produk": nama_produk,
        "jumlah" : jumlah,
        "deskripsi" : deskripsi,
        "jenis" : jenis,
        "status" : status
    })
    with open ("data/supply.json", "w") as edit_file:       
        json.dump(data, edit_file, indent=4)
    return (data)


@app.put("/supply/{supply_id}", dependencies=[Depends(JWTBearer())])
async def update_supply(supply_id: int,
        nama_produk: str,
        jumlah: int,
        deskripsi: str,
        jenis: str,
        status: str
    ):
    with open("data/supply.json", "r+") as read_file:
        data = json.load(read_file)
    elementIdx = -1
    for idx, dataEl in enumerate(data):
        if (dataEl["id"] == supply_id):
            elementIdx = idx
    if (elementIdx == -1):
        raise HTTPException(status_code=404, detail=f'Item not found')

    else :
        data[elementIdx] = {
            "id": supply_id,
            "nama_produk": nama_produk,
            "jumlah" : jumlah,
            "deskripsi" : deskripsi,
            "jenis" : jenis,
            "status" : status
        }
    with open ("data/supply.json", "w") as edit_file:       
        json.dump(data, edit_file, indent=4)
    return (data)

@app.delete("/supply/{supply_id}", dependencies=[Depends(JWTBearer())])
async def delete_a_supply(supply_id: int):
    with open("data/supply.json", "r+") as read_file:
        data = json.load(read_file)
    for idx, dataEl in enumerate(data):
        if (dataEl["id"] == supply_id):
            del data[idx]
    
    with open ("data/supply.json", "w") as edit_file:       
        json.dump(data, edit_file, indent=4)
    return (data)

@app.delete("/supply", dependencies=[Depends(JWTBearer())])
async def delete_supplies():
    with open ("data/supply.json", "w") as edit_file:       
        json.dump([], edit_file, indent=4)
    return ([])

# API bagian Produksi
@app.get("/production", dependencies=[Depends(JWTBearer())])
async def get_all_productions():
    with open("data/production.json", "r+") as read_file:
        data = json.load(read_file)
    if len(data) < 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Supplies were found")
    return data

@app.get("/production/{production_id}", dependencies=[Depends(JWTBearer())])
async def get_a_production(production_id:int):
    with open("data/production.json", "r+") as read_file:
        data = json.load(read_file)
    for menu_item in data:
        if menu_item['id'] == production_id:
            return menu_item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supply Not Found")


@app.post("/production", dependencies=[Depends(JWTBearer())])
async def add_production(
        status_produksi: str,
        id_produk: str
    ):
    with open("data/production.json", "r+") as read_file:
        data = json.load(read_file)
    newItemId = data[-1]["id"]+1 if len(data) > 0 else 1
    data.append({
        "id": newItemId,
        "status_produksi": status_produksi,
        "id_produk": id_produk
    })
    with open ("data/production.json", "w") as edit_file:       
        json.dump(data, edit_file, indent=4)
    return (data)


@app.put("/production/{production_id}", dependencies=[Depends(JWTBearer())])
async def update_supply(production_id: int,
        status_produksi: str,
        id_produk: str
    ):
    with open("data/production.json", "r+") as read_file:
        data = json.load(read_file)
    elementIdx = -1
    for idx, dataEl in enumerate(data):
        if (dataEl["id"] == production_id):
            elementIdx = idx
    if (elementIdx == -1):
        raise HTTPException(status_code=404, detail=f'Item not found')

    else :
        data[elementIdx] = {
            "id": production_id,
            "status_produksi": status_produksi,
            "id_produk": id_produk
        }
    with open ("data/production.json", "w") as edit_file:       
        json.dump(data, edit_file, indent=4)
    return (data)

@app.delete("/production", dependencies=[Depends(JWTBearer())])
async def delete_all_productions():
    with open ("data/production.json", "w") as edit_file:       
        json.dump([], edit_file, indent=4)
    return ([])

@app.delete("/production/{production_id}", dependencies=[Depends(JWTBearer())])
async def delete_a_production(production_id: int):
    with open("data/production.json", "r+") as read_file:
        data = json.load(read_file)
    for idx, dataEl in enumerate(data):
        if (dataEl["id"] == production_id):
            del data[idx]
    
    with open ("data/production.json", "w") as edit_file:       
        json.dump(data, edit_file, indent=4)
    return (data)

# API bagian Penjualan
@app.get("/penjualan", dependencies=[Depends(JWTBearer())])
async def get_all_sellings():
    with open("data/penjualan.json", "r+") as read_file:
        data = json.load(read_file)
    if len(data) < 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Supplies were found")
    return data

@app.get("/penjualan/{selling_id}", dependencies=[Depends(JWTBearer())])
async def get_a_selling(selling_id:int):
    with open("data/penjualan.json", "r+") as read_file:
        data = json.load(read_file)
    for menu_item in data:
        if menu_item['id'] == selling_id:
            return menu_item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supply Not Found")


@app.post("/penjualan", dependencies=[Depends(JWTBearer())])
async def add_penjualan(
        jumlah_penjualan: int,
        pendapatan: int,
        status: int
    ):
    with open("data/penjualan.json", "r+") as read_file:
        data = json.load(read_file)
    newItemId = data[-1]["id"]+1 if len(data) > 0 else 1
    data.append({
        "id": newItemId,
        "jumlah_penjualan": jumlah_penjualan,
        "pendapatan": pendapatan,
        "status" : status
    })
    with open ("data/penjualan.json", "w") as edit_file:       
        json.dump(data, edit_file, indent=4)
    return (data)

@app.put("/penjualan/{selling_id}", dependencies=[Depends(JWTBearer())])
async def update_penjualan(selling_id: int, 
        jumlah_penjualan: int,  
        pendapatan: int,
        status: int
    ):
    with open("data/penjualan.json", "r+") as read_file:
        data = json.load(read_file)
    elementIdx = -1
    for idx, dataEl in enumerate(data):
        if (dataEl["id"] == selling_id):
            elementIdx = idx
    if (elementIdx == -1):
        raise HTTPException(status_code=404, detail=f'Item not found')

    else :
        data[elementIdx] = {
            "id": selling_id,
            "jumlah_penjualan": jumlah_penjualan,
            "pendapatan": pendapatan,
            "status" : status
        }
    with open ("data/penjualan.json", "w") as edit_file:       
        json.dump(data, edit_file, indent=4)
    return (data)

@app.delete("/penjualan/{selling_id}", dependencies=[Depends(JWTBearer())])
async def delete_a_penjualan(selling_id: int):
    with open("data/penjualan.json", "r+") as read_file:
        data = json.load(read_file)
    for idx, dataEl in enumerate(data):
        if (dataEl["id"] == selling_id):
            del data[idx]
    
    with open ("data/penjualan.json", "w") as edit_file:       
        json.dump(data, edit_file, indent=4)
    return (data)

@app.delete("/penjualan", dependencies=[Depends(JWTBearer())])
async def delete_penjualan():
    with open ("data/penjualan.json", "w") as edit_file:       
        json.dump([], edit_file, indent=4)
    return ([])


# API bagian pembeli
@app.get("/pembeli", dependencies=[Depends(JWTBearer())])
async def get_all_buyers():
    with open("data/pembeli.json", "r+") as read_file:
        data = json.load(read_file)
    if len(data) < 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Supplies were found")
    return data

@app.get("/pembeli/{buyer_id}", dependencies=[Depends(JWTBearer())])
async def get_a_buyer(buyer_id:int):
    with open("data/pembeli.json", "r+") as read_file:
        data = json.load(read_file)
    for menu_item in data:
        if menu_item['id'] == buyer_id:
            return menu_item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supply Not Found")


@app.post("/pembeli", dependencies=[Depends(JWTBearer())])
async def add_buyer(
    nama_pembeli: str,
    umur: int,
    gender: str,
    alamat: str,
    no_telp:str,
    email: str
):
    with open("data/pembeli.json", "r+") as read_file:
        data = json.load(read_file)
    newItemId = data[-1]["id"]+1 if len(data) > 0 else 1
    data.append({
        "id": newItemId,
        "nama_pembeli": nama_pembeli,
        "umur": umur,
        "gender": gender,
        "alamat": alamat,
        "no_telp":no_telp,
        "email": email
    })
    with open ("data/pembeli.json", "w") as edit_file:       
        json.dump(data, edit_file, indent=4)
    return (data)

@app.put("/pembeli/{buyer_id}", dependencies=[Depends(JWTBearer())])
async def update_buyer(buyer_id: int, 
        nama_pembeli: str,
        umur: int,
        gender: str,
        alamat: str,
        no_telp:str,
        email: str
    ):
    with open("data/pembeli.json", "r+") as read_file:
        data = json.load(read_file)
    elementIdx = -1
    for idx, dataEl in enumerate(data):
        if (dataEl["id"] == buyer_id):
            elementIdx = idx
    if (elementIdx == -1):
        raise HTTPException(status_code=404, detail=f'Item not found')

    else :
        data[elementIdx] = {
            "id": buyer_id,
            "nama_pembeli": nama_pembeli,
            "umur": umur,
            "gender": gender,
            "alamat": alamat,
            "no_telp":no_telp,
            "email": email
        }
    with open ("data/pembeli.json", "w") as edit_file:       
        json.dump(data, edit_file, indent=4)
    return (data)

@app.delete("/pembeli/{buyer_id}", dependencies=[Depends(JWTBearer())])
async def delete_a_buyer(buyer_id: int):
    with open("data/pembeli.json", "r+") as read_file:
        data = json.load(read_file)
    for idx, dataEl in enumerate(data):
        if (dataEl["id"] == buyer_id):
            del data[idx]
    
    with open ("data/pembeli.json", "w") as edit_file:       
        json.dump(data, edit_file, indent=4)
    return (data)

@app.delete("/pembeli", dependencies=[Depends(JWTBearer())])
async def delete_all_buyer():
    with open ("data/pembeli.json", "w") as edit_file:       
        json.dump([], edit_file, indent=4)
    return ([])
