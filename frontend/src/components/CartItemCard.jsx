import { Card, Flex } from "antd"
import { useNavigate } from "react-router-dom";

function CartItemCard({item}) {
    const product = item.product;

    const navigate = useNavigate();

    return (
        <Card
            onClick={() => navigate(`/product/${product.id}`, {replace: true})}
            style={{width: "100%", cursor: "pointer"}}
        >
            <Flex
                justify="space-between"
            >
                <Flex>
                    <div style={{width: "100px", height: "100px"}}>
                        <img src={product.images[0]["image"]} style={{height: "100%", width: "100px", objectFit:"contain"}}/>
                    </div>
                    <div>
                        <p>{product.name}</p>
                        <p>{product.price}</p>
                    </div>
                </Flex>
                <div>
                    <p>Quantity: {item.quantity}</p>
                    <p>Total: {product.price * item.quantity}.000 VND</p>
                </div>
            </Flex>
        </Card>
    )
}

export default CartItemCard