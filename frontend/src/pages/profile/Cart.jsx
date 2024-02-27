import { ShoppingCartOutlined, ShoppingOutlined } from "@ant-design/icons";
import { Flex, Button } from "antd";
import { useContext, useEffect, useState } from "react";
import URL from "../../api/urls";
import AuthContext from "../../contexts/AuthContext";
import CartItemCard from "../../components/CartItemCard";
import { useNavigate } from "react-router-dom";

function Cart() {
    const { authToken } = useContext(AuthContext);
    const [cartItems, setCartItems] = useState([]);

    const navigate = useNavigate();

    const deleteItem = async (itemID) => {
        console.log("You shall not pass", itemID)
    };

    const createOrder = async () => {
        const products = [];
        cartItems.map((item) => {
            products.push({
                "product_id": item.product["id"],
                "quantity": item.quantity
            })
        })
        
        navigate(`/create-order/`, {replace: true, state:{products}})
    }

    useEffect(() => {
        const fetchCart = async () => {
            let res = await fetch(URL.User + "cart/", {
                headers: {
                    "Authorization": `Bearer ${String(authToken.access)}`
                },
            })
            let data = await res.json()
            if (res.status === 200) {
                setCartItems(data)
            }
        }

        fetchCart()
    }, [])

    return (
        <>
            <h1>Cart <ShoppingCartOutlined /></h1>
            <Flex
                gap={20}
                wrap="wrap"
            >
            {cartItems.length === 0 ?
                <div>
                    <p>No items found</p>        
                </div>
                    :
                    cartItems.map((item) => (
                        <CartItemCard key={item.id} item={item} deleteItem={deleteItem} />
                ))
            }
            </Flex>
            <Button
                onClick={createOrder}
                style={{ float: "right", marginTop: "15px" }}
                icon={<ShoppingOutlined />}
            >
                Create Order
            </Button>
        </>
    )
}

export default Cart;