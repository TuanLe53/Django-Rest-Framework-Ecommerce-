import { Card, Flex } from "antd"
import { useNavigate } from "react-router-dom";
import { DeleteFilled } from "@ant-design/icons";

function CartItemCard({item, deleteItem}) {
    const product = item.product;

    const navigate = useNavigate();

    const handleDelete = () => {
        deleteItem(item.id)
    }

    return (
        <Card
            style={{width: "100%", cursor: "pointer"}}
        >
            <Flex
                justify="space-between"
            >
                <Flex
                    onClick={() => navigate(`/product/${product.id}`, {replace: true})}
                >
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
            <DeleteFilled
                style={{
                    color: "red",
                    fontSize: 24,
                    position: "absolute",
                    top: 10,
                    right: 20
                }}
                onClick={handleDelete}
            />
        </Card>
    )
}

export default CartItemCard