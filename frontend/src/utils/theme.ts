import { extendTheme } from '@chakra-ui/react'

const theme = extendTheme({
    colors: {
        brand: {
            blue: {
                800: "#1A3560",
                300: "#449DD1",
                100: "#EAF4F6"
            },
            orange: {
                400: "#EA9010"
            },
            green: {
                600: "#003844",
                200: "#00647A",
                900: "#828C51"
            },
            white: {
                100: "#ffffff"
            }
        }
    },
    styles: {
        global: {
            body: {
                bg: "brand.blue.100",
                color: "black",
            }
        }
    },
    fonts: {
        heading: `'Poppins', sans-serif`,
        body: `'Open Sans', sans-serif`
    }
})

export default theme