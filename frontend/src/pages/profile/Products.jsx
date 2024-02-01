import { Flex, Button, Modal, Form, Input, InputNumber, Select, Upload, Checkbox } from "antd";
import { PlusOutlined } from "@ant-design/icons";
import { useContext, useEffect, useState } from "react";
import AuthContext from "../../contexts/AuthContext";
import URL from "../../api/urls";
import ProductCard from "../../components/ProductCard";

function Products() {
    const { authToken } = useContext(AuthContext);
    const [products, setProducts] = useState([]);

    const [isConfirm, setIsConfirm] = useState(false);

    const [isOpen, setIsOpen] = useState(false);
    const [form] = Form.useForm();
    const [fileList, setFileList] = useState(null);
    const handleChange = ({fileList}) => {
        setFileList(fileList)
    }

    const [previewVisible, setPreviewVisible] = useState(false);
    const [previewImage, setPreviewImage] = useState("");
    const handlePreview = (file) => {
        setPreviewVisible(true);
        setPreviewImage(file.thumbUrl);
    };

    const handleCancel = () => {
        setIsConfirm(false)
        setIsOpen(false)
        setFileList(null)
    }

    const handleSubmit = async (formValues) => {
        if (!isConfirm) {
            alert("Please make sure you check everything")
            return;
        }
        if (!fileList) {
            setIsConfirm(false)
            return alert("Please upload your product's images");
        }
        let data = new FormData();
        for (const item in formValues) {
            data.append(item, formValues[item])
        }
        for (const file in fileList) {
            data.append("images", fileList[file]["originFileObj"])
        }
        let res = await fetch(URL.Product, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${String(authToken.access)}`
            },
            body: data
        })
        if (res.status === 201) {
            setIsOpen(false)
            setFileList(null)
            form.resetFields()
        } else {
            alert("Something went wrong!")
        }
    }

    useEffect(() => {
        const fetchProducts = async () => {
            let res = await fetch(URL.Product, {
                headers: {
                    "Authorization": `Bearer ${String(authToken.access)}`
                },
            })
            let data = await res.json()
            if (res.status === 200) {
                setProducts(data)
            }
        }

        fetchProducts()
    }, [])

    return (
        <>
            <Flex
                justify="space-between"
                align="center"
            >
                <h1>Products</h1>
                <Button
                    type="primary"
                    onClick={() => setIsOpen(true)}
                    icon={<PlusOutlined />}>
                    Add Item
                </Button>
            </Flex>

            <Flex
                gap={20}
                wrap="wrap"
            >
                {products.length === 0
                    ?
                    <>
                        You don't have any products yet
                    </>
                    :
                    products.map((item) => (
                    <ProductCard item={item} width={200} />
                ))}
            </Flex>

            <Modal
                title="Add Product"
                open={isOpen}
                onOk={form.submit}
                onCancel={handleCancel}
            >
                <Form
                    form={form}
                    name="add product"
                    onSubmit={e => e.preventDefault()}
                    onFinish={handleSubmit}
                >
                    <Form.Item
                        name="name"
                        label="Product name"
                        rules={[
                            {
                                required: true,
                                message: "Please input your product's name"
                            },
                            {
                                type: "string",
                                message: "The input value must be string"
                            }
                        ]}
                    >
                        <Input />
                    </Form.Item>

                    <Form.Item
                        name="sku"
                        label="SKU"
                        rules={[
                            {
                                required: true,
                                message: "Please input your product's SKU"
                            },
                            {
                                type: "string",
                                message: "The input value must be string"
                            }
                        ]}
                    >
                        <Input />
                    </Form.Item>

                    <Form.Item
                        name="description"
                        label="Description"
                        rules={[
                            {
                                required: true,
                                message: "Please input your product's description"
                            },
                            {
                                type: "string",
                                message: "The input value must be string"
                            }
                        ]}
                    >
                        <Input />
                    </Form.Item>

                    <Form.Item
                        name="price"
                        label="Price"
                        rules={[
                            {
                                required: true,
                                message: "Please input your product's price"
                            },
                            {
                                type: "number",
                                message: "The input is not a valid number"
                            }
                        ]}
                    >
                        <InputNumber />
                    </Form.Item>

                    <Form.Item
                        name="quantity"
                        label="Quantity"
                        rules={[
                            {
                                required: true,
                                message: "Please input your product's quantity"
                            },
                            {
                                type: "number",
                                message: "The input is not a valid number"
                            }
                        ]}
                    >
                        <InputNumber />
                    </Form.Item>

                    <Form.Item
                        name="category"
                        label="Category"
                        rules={[
                            {
                                required: true,
                                message: "Please input your product's quantity"
                            }
                        ]}
                    >
                        <Select>
                            <Select.Option value="food">Food</Select.Option>
                            <Select.Option value="t-shirt">T-Shirt</Select.Option>
                            <Select.Option value="ice-cream">Ice cream</Select.Option>
                        </Select>
                    </Form.Item>

                    <Form.Item
                        label="Product's images"
                    >
                        <Upload
                            listType="picture-card"
                            fileList={fileList}
                            multiple
                            onChange={handleChange}
                            onPreview={handlePreview}
                            beforeUpload={() => false}
                        >
                            <button>
                                <PlusOutlined />
                                <div>Upload</div>
                            </button>
                        </Upload>
                    </Form.Item>

                    <Checkbox checked={isConfirm} onChange={()=>setIsConfirm(!isConfirm)}>I have check everything</Checkbox>

                </Form>

            </Modal>
        </>
    )
}

export default Products;