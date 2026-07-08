import { useEffect, useState } from "react";
import BasicLayout from "../components/BasicLayout"
import { useAuth } from "../context/AuthContext"
import { Box, Heading, Text, HStack, VStack, Icon, IconButton } from "@chakra-ui/react";
import { FaRegTrashAlt, FaRecycle, FaLeaf, FaCouch} from "react-icons/fa";
import { IoLocation } from "react-icons/io5";
import { apiAuth } from "../utils/api";
import type { Schedule } from "../utils/helper";


export default function SchedulePage() {
    const { user } = useAuth();
    const addresses = user?.addresses
    const [schedules, setSchedules] = useState<Schedule[]>([]);
    useEffect(() => {
        const getSchedules = async () => {
        if (!addresses) return;
        try {
            const responses = await Promise.all(addresses.map(async address => {
                return (await apiAuth.get(`/api/addresses/${address.id}/schedule`)).data;
            }))
            setSchedules(responses)
        } catch(error) {
            return error;
        }
    }
    getSchedules();
    }, [addresses])
    console.log(schedules)
    return (
        <>
        <BasicLayout>
        <Heading size={"lg"} my={2}>Your Sanitation Schedule</Heading>
        {addresses ? <VStack align={"start"} spacing={4}>
        {addresses.map((address) =>
        <Box>
            <HStack borderRadius={"2xl"} borderColor={"black"} borderStyle={"solid"} borderWidth={"thin"} padding={4} my={4}>
            <Icon as={IoLocation}/>
            <Heading size={"sm"} color={"teal.800"} fontWeight={"extrabold"}>ADDRESS:</Heading>
            <Heading size={"sm"} color={"teal.800"} key={address.id}>
                {address.street_address}, {address.city}, {address.state}, {address.zip_code}
            </Heading>
            </HStack>
            <VStack align={"start"} spacing={2}>
            
            <HStack>
            <IconButton
                isRound={true}
                variant="solid"
                bg={"brand.blue.300"}
                color={"brand.green.600"}
                aria-label={"trash"}
                boxSize={"10"}
                icon={<FaRegTrashAlt/>}
            />
            <Text fontWeight={"semibold"}>Trash:</Text>
            <Text>{schedules.find((schedule) => schedule.id === address.schedule_id)?.days_trash.join(", ").toUpperCase()} </Text>
            </HStack>

            <HStack>
             <IconButton
                isRound={true}
                variant="solid"
                bg={"brand.blue.300"}
                color={"brand.green.600"}
                aria-label={"trash"}
                boxSize={"10"}
                icon={<FaRecycle/>}
            />
            <Text fontWeight={"semibold"}>Recycling:</Text>
            <Text>{schedules.find((schedule) => schedule.id === address.schedule_id)?.days_recycling.join(", ").toUpperCase()}</Text>
            </HStack>

            <HStack>
            <IconButton
                isRound={true}
                variant="solid"
                bg={"brand.blue.300"}
                color={"brand.green.600"}
                aria-label={"trash"}
                boxSize={"10"}
                icon={<FaLeaf/>}
            />
            <Text fontWeight={"semibold"}>Compost:</Text>
            <Text>{schedules.find((schedule) => schedule.id === address.schedule_id)?.days_compost.join(", ").toUpperCase()}</Text>
            </HStack>

            <HStack>
            <IconButton
                isRound={true}
                variant="solid"
                bg={"brand.blue.300"}
                color={"brand.green.600"}
                aria-label={"trash"}
                boxSize={"10"}
                icon={<FaCouch/>}
            />
            <Text fontWeight={"semibold"}>Large Items:</Text>
            <Text>{schedules.find((schedule) => schedule.id === address.schedule_id)?.days_large_items.join(", ").toUpperCase()}</Text>
            </HStack>
            </VStack>
        </Box>
        )}
        </VStack>
        : <p>Address: No address saved yet</p>}
        </BasicLayout>
        </>

    )
}