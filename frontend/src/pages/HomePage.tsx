import { 
    VStack, 
    Text, 
    Card, 
    CardHeader, 
    CardBody, 
    Button, 
    HStack, 
    Icon, 
    Heading, 
    Container, 
    Center, 
} from "@chakra-ui/react"
import { FaBell, FaSearch, FaCalendar } from "react-icons/fa"
import { Link as ReactLink } from "react-router"

const featureCards = [
    {icon: FaSearch, label: "Search for Items"},
    {icon: FaBell, label: "Get Text Reminders"},
    {icon: FaCalendar, label: "Check NYC Collection Status"},
]

export default function HomePage() {
    return  (
        <VStack spacing={6} minH={"100vh"} justifyContent={"center"}>
        <Heading size={"2xl"}>Trash Guide NYC</Heading>
        <Container maxW={"container.md"} centerContent>
        <Text fontSize={"xl"} color={"brand.green.200"} fontWeight={"normal"}>Access NYC sanitation information in one place.
        </Text>
        </Container>
        <HStack spacing={4}>
        {featureCards.map(({ icon, label }) =>
            <Card key={label} fontWeight={"bold"} borderRadius={"3xl"} minW={"3xs"} maxWidth={"2xs"}>
                <CardHeader><Center><Icon as={icon} color={"brand.green.200"} boxSize={8}/></Center></CardHeader>
                <CardBody><Center><Text fontWeight={"medium"}>{label}</Text></Center></CardBody>
            </Card>
        )}
        </HStack>
        <Button
        mt={10}
        bg={"brand.orange.400"}
        variant={"solid"}
        borderRadius={"3xl"}
        color={"white"}
        fontWeight={"bold"}
        size={"lg"}
        px={20}
        as={ReactLink}
        to={"/search"}
        >
            Get Started
        </Button>
        </VStack>
    )

}
