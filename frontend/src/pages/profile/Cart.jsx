import { ShoppingCartOutlined } from "@ant-design/icons";
import { Flex } from "antd";
import { useContext, useEffect, useState } from "react";
import URL from "../../api/urls";
import ProductCard from "../../components/ProductCard";
import AuthContext from "../../contexts/AuthContext";

function Cart() {
    const { authToken } = useContext(AuthContext);
    const [cartItems, setCartItems] = useState([]);

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
                    <ProductCard item={item.product} width={200} key={item.id}/>
                ))
            }
            </Flex>
        </>
    )
}

export default Cart;