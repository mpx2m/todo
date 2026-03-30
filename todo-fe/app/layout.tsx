import type { Metadata } from "next"
import { Geist, Geist_Mono } from "next/font/google"
import "./globals.css"
import { ReactQueryProvider } from "./ReactQueryProvider"
import { AntdRegistry } from "@ant-design/nextjs-registry"

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
})

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
})

export const metadata: Metadata = {
  title: "Todo App",
  description:
    "Next.js Todo App: Organize, track and complete tasks effortlessly",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html
      lang="en"
      suppressHydrationWarning
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">
        <AntdRegistry>
          <ReactQueryProvider>{children}</ReactQueryProvider>
        </AntdRegistry>
      </body>
    </html>
  )
}
