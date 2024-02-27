import { Card, Flex } from "antd";
import { Link } from "react-router-dom";

function OrderCard() {
    
    return (
        <Link>
            <Card
                title="WN29032ASD"
                extra="Delivered"
            >
                <Flex
                    justify="space-between"
                >
                    <p>Created at: 19-01-2017</p>
                    <p>Total: 219.000 VND</p>
                </Flex>
            </Card>
        </Link>
    )
}

function Orders() {
    const orders = [1, 2, 3, 4];

    return (
        <>
            <h1>Orders</h1>
            {orders.length === 0 ?
            <p>You have no order</p>
                :
            <>
                <p>You have {orders.length} orders</p>
                {orders.map((order) =>(
                    <OrderCard key={order} />
                ))}
            </>
            }
        </>
    )
}

export default Orders;