import { motion } from "framer-motion"

interface ProfileSectionProps {
  name: string
  bio: string
  imageUrl: string
}

export function ProfileSection({ name, bio, imageUrl }: ProfileSectionProps) {
  return (
    <div className="flex flex-col items-center text-center">
      <motion.div
        whileHover={{ scale: 1.04 }}
        whileTap={{ scale: 0.96 }}
        transition={{ type: "spring", stiffness: 500, damping: 25 }}
        className="relative"
      >
        <div
          className="relative h-24 w-24 overflow-hidden rounded-full"
          style={{
            background: "rgba(255, 255, 255, 0.5)",
            backdropFilter: "blur(10px)",
            WebkitBackdropFilter: "blur(10px)",
            boxShadow: `
              inset 0 2px 4px rgba(255, 255, 255, 0.8),
              0 0 0 2px rgba(255, 255, 255, 0.6),
              0 4px 16px rgba(0, 0, 0, 0.1),
              0 12px 32px rgba(120, 119, 198, 0.15)
            `,
          }}
        >
          <img
            src={imageUrl || "/placeholder.svg"}
            alt={name}
            className="h-full w-full object-cover"
          />
        </div>

        <div
          className="absolute inset-0 rounded-full pointer-events-none"
          style={{
            boxShadow: "0 0 40px 8px rgba(120, 119, 198, 0.1)",
          }}
        />
      </motion.div>

      <h1 className="mt-5 text-xl font-semibold tracking-tight text-gray-800">{name}</h1>
      <p className="mt-2 text-sm text-gray-500">{bio}</p>
    </div>
  )
}
