import { Card, Flex } from "antd";
import { Link } from "react-router-dom";

const { Meta } = Card;

function ProductCard({ item, width }) {

    return (
        <Link to={`/product/${item.id}`}>        
            <Card
                style={{ width: width }}
                hoverable
                cover={
                    <div style={{overflow: "hidden", height: "200px"}}>
                        <img style={{height:"100%", width:width, objectFit: "contain"}} alt={`${item.name}'s image`} src={item.images[0]["image"]} />
                    </div>
                }
            >
                <Meta title={item.name} />
                <Flex
                    justify="space-between"
                >
                    <p>{item.price} VND</p>
                    <p>{item.rating}<span>&#9733;</span></p>    
                </Flex>
            </Card>
        </Link>
    )
}

export default ProductCard;