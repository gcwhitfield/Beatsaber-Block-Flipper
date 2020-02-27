using System;
using Mono.Cecil;

// some info on dotnet console apps
// https://docs.microsoft.com/en-us/dotnet/core/tutorials/cli-create-console-app

namespace BeatSaberModLauncher
{
    class Program
    {
        static void Mod1()
        {
            // do some stuff
        }

        static void Mod2()
        {
            // do some stuff
        }

        static void Main(string[] args)
        {
            Console.WriteLine("Beat Saber Mod Loader");

            // can only pass in one argument
            if (args.Length > 1)
            {
                Console.WriteLine("Can only pass one argument");
            }

            switch (args[0])
            {
                case "1":
                    Mod1();
                    break;

                case "2":
                    Mod2();
                    break;

                default:
                    Console.WriteLine("The only valid arguments are 1 and 2");
                    Console.WriteLine("1 = cognitiviely engaging mod.");
                    Console.WriteLine("2 = sedentary mod.");
                    break;
            }
        } 
    }
}
