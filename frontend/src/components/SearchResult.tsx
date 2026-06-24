import { Box, Card, CardHeader, CardBody, CardFooter, Text, Heading, HStack } from '@chakra-ui/react'
import { FaRecycle, FaRegTrashAlt, FaLeaf, FaCouch } from 'react-icons/fa'
import { IoIosWarning } from "react-icons/io";
import type { ResultProps } from '../utils/helper'

export default function SearchResult( { data }: ResultProps) {
    const categoryStyle = [
        {icon: <FaRegTrashAlt/>, label: "Trash", bgColor:"gray.300", color: "gray.900"},
        {icon: <FaRecycle/>, label: "Recycling", bgColor: "green.200", color: "white"},
        {icon: <FaLeaf/>, label: "Compost", bgColor: "yellow.900", color: "white"},
        {icon: <FaCouch/>, label: "Large Items", bgColor: "blue.300", color: "blue.900"},
        {icon: <IoIosWarning/>, label: "Special", bgColor: "orange.300", color: "orange.900"}
    ]
    return (
        <Box>
        {data.length === 0 ?
            <Card>
                <CardHeader></CardHeader>
                <CardBody>
                    <Text>No Results Found Contact 311 for accurate disposal instructions</Text>
                </CardBody>
            </Card>:
            <Box pt={10}>
            {data.map((item) =>
                <Card key={item.category_name} width={"xl"} maxW={"container.2xl"} borderRadius={"3xl"}>
                <CardHeader 
                bg={categoryStyle.find(style => style.label == item.col_type)?.bgColor} 
                borderTopRadius={"3xl"}>
                <HStack>
                    {categoryStyle.find(style => style.label == item.col_type)?.icon}
                    <Heading 
                        size={"md"} 
                        fontWeight={"extrabold"}>
                            {item.col_type}
                        </Heading>
                </HStack>
                </CardHeader>
                <CardBody px={8} py={6}>
                    <Text fontSize={"xl"} fontWeight={"medium"}>{item.disposal_instructions}</Text>
                </CardBody>
            </Card>
            )}
            </Box>
        }
    </Box>
    )
}