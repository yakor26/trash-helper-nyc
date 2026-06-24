import { GridItem, Button } from "@chakra-ui/react"
import { IoAddCircleOutline } from "react-icons/io5"

interface ExampleSearchProps {
    onSearchClick: (search: string) => void
    onSearchSubmit: (search: string) => void
}
export default function ExampleItems({ onSearchClick, onSearchSubmit }: ExampleSearchProps) {
    const exampleSearch = async (search: string) => {
        onSearchClick(search)
        onSearchSubmit(search)
    }
    const exampleItems = [
        {item: "Old Couch"},
        {item: "AA Battery"},
        {item: "Cell Phone"},
        {item: "Indoor Fan"},
        {item: "Pizza Box"},
        {item: "Glass Jar"},
    ]

    return (
        <>
        {exampleItems.map((value) =>
                <GridItem colSpan={1} rowSpan={1} key={value.item}>
                    <Button leftIcon={<IoAddCircleOutline color={"teal"} fontSize={"24"}/>} 
                    fontSize={"lg"} 
                    color={"black"} 
                    px={28} 
                    py={6} 
                    variant='outline'
                    borderColor={"blackAlpha.600"}
                    borderRadius={"3xl"}
                    onClick={()=> exampleSearch(value.item)}>
                        {value.item}
                    </Button>
                </GridItem>
                )}
        </>
        )
    }