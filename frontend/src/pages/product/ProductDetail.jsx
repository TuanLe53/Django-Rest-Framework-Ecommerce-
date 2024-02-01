import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import {StarFilled} from "@ant-design/icons";
import URL from "../../api/urls";
import { Carousel, Flex, Image, Layout, Spin } from "antd";
import "./product_detail.css";

const { Content, Sider } = Layout;

const imgContainerStyle = {
    backgroundColor: "white",
}
const infoContainerStyle = {
    paddingLeft: "50px"
}

function ProductDetail() {
    const { id } = useParams();
    const [product, setProduct] = useState(); 
    const [isLoading, setIsLoading] = useState(true);
    console.log(product)
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
                    </Content>
                </>
                    
            }
            </Layout>

        </Layout>
    )
}

export default ProductDetail;