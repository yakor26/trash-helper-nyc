import { Box, Card, CardHeader, CardBody, CardFooter, Text } from '@chakra-ui/react'
import type { ResultProps } from '../utils/helper'
export default function SearchResult( { data }: ResultProps) {
    return (
        <Box>
        {data.length === 0 ?
            <Card>
                <CardHeader></CardHeader>
                <CardBody>
                    <Text>No Results Found</Text>
                </CardBody>
            </Card>:
            <Box>
            {data.map((item) =>
                <Card>
                <CardHeader>{item.category_name}</CardHeader>
                <CardBody>
                    <Text>{item.disposal_instructions}</Text>
                </CardBody>
            </Card>
            )}
            </Box>
        }
    </Box>
    )
}