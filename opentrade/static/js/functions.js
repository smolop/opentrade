function bindCloseOrderBtn(){
    $(".close-order-button").click(removeOrderRow);
}

function removeOrderRow(e) {
    Promise.resolve(closeOrder(e));

}

async function getPortfolio(){
    console.log("HERE!!!");
    const url = '{{ BASE_URL }}/api/portfolio/all/';
    await fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type': 'application/json',
            'Authorization': 'Token {{token}}',
        }})
        .then((res) => {
            return res.json();})
        .then((assets) => {
            renderTable(assets.shares)
        });

}

function getValue(e) {
    console.log(e.target.value);
    return e.target.value;
}

async function closeOrder(e){
    const obj_val = getValue(e);
    const url = '{{ BASE_URL }}/api/shares/close/';
    const data = { ref: obj_val };
    await fetch(url, {
        method: 'POST', // or 'PUT'
        body: JSON.stringify(data), // data can be `string` or {object}!
        headers:{
            'Content-Type': 'application/json',
            'Authorization': 'Token {{token}}',
        }
    }).then(function (res) {
        if(res.status >= 200 && res.status < 400){
            alert(" [Successful operation]\n [Close order]");

            $("#tr-"+obj_val).remove();
        }else{
            alert("Failed operation");
        }
    });

}

async function getPortfolio(){
    console.log("HERE!!!");
    const url = '{{ BASE_URL }}/api/portfolio/all/';
    await fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type': 'application/json',
            'Authorization': 'Token {{token}}',
        }})
        .then((res) => {
            return res.json();})
        .then((assets) => {
            renderTable(assets.shares)
        });

}

function renderTable(assets){
    const html = assets.map(asset => {
        const order_id = asset.ref;
        const symbol = asset.symbol;
        const operation = asset.operation;
        const date = asset.date;
        const timestamp = asset.timestamp;
        const quantity = asset.quantity;
        const price = asset.price;
        const total = quantity*price;
        return `
                <tr id="tr-${order_id}">
                    <td>${symbol}</td>
                    <td>${operation}</td>
                    <td>${date}</td>
                    <td>${timestamp}</td>
                    <td>${quantity}</td>
                    <td>${price}</td>
                    <td>${total}</td>
                    <td>
                            <button
                                type="button"
                                class="btn btn-primary close-order-button"
                                value="${order_id}"
                                id="close-btn-${order_id}"
                                >
                            Close order
                            </button>
                    </td>
                </tr>
                `;
    });
    $("#tbody-orders").html(html);
    bindCloseOrderBtn()
}