import { useContext, useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { StarFilled, ShoppingCartOutlined, ShoppingOutlined  } from "@ant-design/icons";
import URL from "../../api/urls";
import { Button, Carousel, Flex, Image, InputNumber, Layout, Spin, notification } from "antd";
import "./product_detail.css";
import AuthContext from "../../contexts/AuthContext";

const { Content, Sider } = Layout;

const imgContainerStyle = {
    backgroundColor: "white",
}
const infoContainerStyle = {
    paddingLeft: "50px"
}

function ProductDetail() {
    const { id } = useParams();
    const { authToken } = useContext(AuthContext);
    const [product, setProduct] = useState(); 
    const [isLoading, setIsLoading] = useState(true);

    const [quantity, setQuantity] = useState(0);

    const [api, contextHolder] = notification.useNotification();
    const showNotification = () => {
        api["success"]({
            message: "Add to cart",
            description: `Added ${quantity} ${product.name}${quantity !== 1 && "s"} to your cart.`,
        });
    };

    const showAlertNotification = () => {
        api["warning"]({
            message: "Quantity error",
            description: "Please check your quantity before adding it to the cart."
        })
    }

    const showErrorNotification = () => {
        api["error"]({
            message: "Server error",
            description: "Something go wrong. Please try again later"
        })
    }

    const addToCart = async () => {
        if (quantity === 0) {
            return showAlertNotification();
        }
        let body = {
            product: product.id,
            quantity: quantity
        };

        let res = await fetch(URL.User + "cart/", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${String(authToken.access)}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
        })
        
        if (res.status === 201) {
            return showNotification();
        } else {
            return showErrorNotification();
        }
    }

    const navigate = useNavigate();
    const handleBuy = () => {
        if (quantity) {
            let products = [{
                "product_id": product.id,
                "quantity": quantity
            }];
            navigate(`/create-order/`, {replace: true, state:{products}})
        }
    }

    useEffect(() => {
        const fetchProduct = async () => {
            let res = await fetch(URL.Server + `product/${id}`)
            let data = await res.json()
            if (res.status === 200) {
                setProduct(data)
            }
            setIsLoading(false)
        }

        fetchProduct()
    }, [])

    return (
        <Layout>
            <Layout>
            {isLoading ? <Spin />
                    :
                <>
                    {contextHolder}        
                    <Sider
                        style={imgContainerStyle}
                        width={"40%"}>
                        <Carousel
                            style={{height: "550px"}}
                            autoplay>
                            {product.images.map((item) => (
                                <div key={item.id}>
                                    <div style={{height: "500px", display: "flex", justifyContent: "center"}}>
                                        <Image style={{height: "100%", objectFit: "contain"}} src={item.image} />
                                    </div>
                                </div>
                            ))}
                        </Carousel>
                    </Sider>
                    <Content style={infoContainerStyle}>
                            <h1>{product.name}</h1>
                            <p>{product.description}</p>
                            <p>Shop: <Link>{product.created_by}</Link></p>
                            <p>In stock: {product.inventory.split(" ")[1]}</p>
                            <p>Price: {product.price} VND</p>
                            <p>Rate: {product.rating}<StarFilled /></p>
                            <Flex>
                                <InputNumber min={1} max={Number(product.inventory.split(" ")[1])} onChange={(value) => setQuantity(value)} />
                                <Button onClick={handleBuy} type="primary" icon={<ShoppingOutlined />}>Buy</Button>
                                <Button onClick={addToCart} icon={<ShoppingCartOutlined />}>Add to Cart</Button>
                            </Flex>
                    </Content>
                </>
                    
            }
            </Layout>

        </Layout>
    )
}

export default ProductDetail;