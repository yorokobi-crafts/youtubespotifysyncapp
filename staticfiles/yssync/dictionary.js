//Dictionary for buttons. So you don't have to read the non-append divs.
var appendTranslations = [
    {
        English: "IGNORE",
        Japanese: "日本語",
        Spanish: "IGNORAR",
    },
    {
        English: "UNDO",
        Japanese: "日本語",
        Spanish: "DESHACER",
    },
];

//Dictionary that contains the translations of every div in the application.
var translations = [
    {
        English: "Switch to Spotify",
        Japanese: "日本語",
        Spanish: "Cambiar a Spotify",
    },
    {
        English: "Log out",
        Japanese: "日本語",
        Spanish: "Cerrar sesión",
    },
    {
        English: "Change user",
        Japanese: "日本語",
        Spanish: "Cambiar usuario",
    },
    {
        English: "Dark mode",
        Japanese: "日本語",
        Spanish: "Tema oscuro",
    },
    {
        English: "Choose your language",
        Japanese: "日本語",
        Spanish: "Selecciona tu lenguaje",
    },
    {
        English: "Settings",
        Japanese: "日本語",
        Spanish: "Configuración",
    },
    {
        English: "Comming soon...",
        Japanese: "日本語",
        Spanish: "Proximamente...",
    },
    {
        English: "English",
        Japanese: "日本語",
        Spanish: "Inglés",
    },
    {
        English: "Japanese",
        Japanese: "日本語",
        Spanish: "Japonés",
    },
    {
        English: "Spanish",
        Japanese: "日本語",
        Spanish: "Español",
    },
    {
        English: "My playlists",
        Japanese: "日本語",
        Spanish: "Mis listas de reproducción",
    },
    {
        English: "Add playlist by URL",
        Japanese: "日本語",
        Spanish: "Agrega listas con URL",
    },
    {
        English: "Ignored items",
        Japanese: "日本語",
        Spanish: "Vídeos ignorados",
    },
    {
        English: "Information",
        Japanese: "日本語",
        Spanish: "Información",
    },
    {
        English: "About us",
        Japanese: "日本語",
        Spanish: "Nosotros",
    },
    {
        English: "Select all",
        Japanese: "日本語",
        Spanish: "Seleccionar todo",
    },
    {
        English: "SYNC",
        Japanese: "日本語",
        Spanish: "SINCRONIZAR",
    },
    {
        English: "This may take a while",
        Japanese: "日本語",
        Spanish: "Esto podría demorar",
    },
    {
        English: "Synchronizing",
        Japanese: "日本語",
        Spanish: "Sincronizando",
    },

    {
        English: "Ignored items:",
        Japanese: "日本語",
        Spanish: "Videos ignorados:",
    },
    {
        English: "No ignored videos",
        Japanese: "日本語",
        Spanish: "No hay videos ignorados",
    },
    {
        English: "My playlist section lets you use the playlists in your Youtube channel. Alternatively, you can paste the URL of the playlist you want to migrate to Spotify in the 'Add playlist by URL' section.",
        Japanese: "日本語",
        Spanish: "La sección 'Mis listas de reproducción' (My playlist) te permite usar las listas en tu canal. Alternativamente puedes usar una URL para agregar la lista que quieres a Spotify en la sección 'Agrega playlist con URL'.",
    },
    {
        English: "By clicking an item in the playlist section, you can see the videos included on each playlist. You can also click the IGNORE button on each video to exclude it in the synchronization process.",
        Japanese: "日本語",
        Spanish: "Al hacer click en un elemento en la sección de listas de reproducción, verás los vídeos incluídos en ella. También puedes clickear el botón IGNORAR para excluir el vídeo en la sincronización.",
    },
    {
        English: "Click the checkbox of the playlist you want to synchronize to your Spotify account. Once you've chosen the playlists you want to synchronize, it's time to click the SYNC button to start the process.",
        Japanese: "日本語",
        Spanish: "Marca los cuadros en las listas que deseas sincronizar a tu cuenta de Spotify. Después de seleccionar las listas, puedes hacer clic en el botón SINCRONIZAR (SYNC) para comenzar el proceso. ",
    },
    {
        English: "You can check your ignored videos any time just by clicking on the Ignored items section. You can revert the ignored videos' status by clicking the UNDO button on each video.",
        Japanese: "日本語",
        Spanish: "Siempre puedes verificar qué videos estás ignorando con solo hacer clic en la sección 'Videos ignorados' (Ignored videos). Puedes revertir el estatus de los vídeos al cliquear el botón DESHACER (UNDO). ",
    },
    {
        English: "Once the process is complete, a box with the process' results will show up, and that's all! Please enjoy your music.",
        Japanese: "日本語",
        Spanish: "Una vez que el proceso se complete, aparecerá una caja con los resultados del proceso y, ¡Eso es todo! Ahora puedes disfrutar de tu música.",
    },
    {
        English: "Prev",
        Japanese: "日本語",
        Spanish: "Anterior",
    },
    {
        English: "Next",
        Japanese: "日本語",
        Spanish: "Siguiente",
    },
    {
        English: "Thank you for using YSSYNC",
        Japanese: "日本語",
        Spanish: "Gracias por utilizar YSSYNC",
    },
    {
        English: "Yolocobi Crafts is a project focused on multimedia, arts, and programming. Our goal is to create compelling projects along with tutorials that can be accessed by anyone. We want our users to enjoy our products and get interested in our projects and learn from them as we develop our abilities. We try every day to master new aspects of the latest technology and make an effort to share our knowledge. Yolocobi Crafts is the result of our team doing their best.",
        Japanese: "日本語",
        Spanish: "Yolocobi Crafts es un proyecto enfocado en las ramas de la multimedia, el arte y la programación. Nuestra meta es crear proyectos atractivos y tutoriales que sean accesibles para todos. Esperamos que nuestros usuarios disfruten nuestros productos y se interesen en nuestros proyectos y que aprendan de ellos, mientras que, al mismo tiempo, nosotros desarrollamos más habilidades. Intentamos dominar nuevos aspectos de la tecnología más actual y hacemos un esfuerzo para compartir nuestro conocimiento. Yolocobi Crafts es el resultado de nuestro equipo dando su máximo esfuerzo.",
    },
    {
        English: "Frequent asked questions:",
        Japanese: "日本語",
        Spanish: "Preguntas frecuentes:",
    },
    {
        English: "What is YSSYNC?",
        Japanese: "日本語",
        Spanish: "¿Qué es YSSYNC?",
    },
    {
        English: "YSSYNC (Youtube-Spotify Synchronizer) is a web application that lets you synchronize your Youtube playlists to Spotify. You can select many playlists at the same time, use URL playlists, and specify videos you don't want to sync from your playlists.",
        Japanese: "日本語",
        Spanish: "YSSYNC (Youtube-Spotify Synchronizer) es una aplicación web que te permite sincronizar tus listas de reproducción de Youtube a Spotify. Puedes seleccionar varias listas al mismo tiempo, utilizar la URL de las listas y especificar qué vídeos no quieres sincronizar.",
    },
    {
        English: "Wich videos am I able to sync?",
        Japanese: "日本語",
        Spanish: "¿Qué videos puedo sincronizar?",
    },
    {
        English: "You can sync a Youtube video as long as it is identified as a song by Youtube. You can tell by checking the description of the video on Youtube and verifying if it has official information about the song. Usually, automatically-made videos can be synchronized.",
        Japanese: "日本語",
        Spanish: "Puedes sincronizar un video de Youtube siempre y cuando esté identificado como una canción por Youtube. Puedes saber si se trata de una canción al leer la descripción del video y verificar la información oficial. Usualmente los vídeos generados automáticamente se pueden sincronizar.",
    },
    {
        English: "What information does YSSYNC get from me?",
        Japanese: "日本語",
        Spanish: "¿A qué información mía tiene acceso YSSYNC?",
    },
    {
        English: "YSSYNC can get access to information from your Youtube account and your Spotify account. You grant it access to information such as playlists, videos, and identification data such as your profile information. YSSYNC can't obtain personal information from your Google account, either from your Spotify account.",
        Japanese: "日本語",
        Spanish: "YSSYNC tiene acceso a información sobre tu cuenta de Youtube y Spotify. La información que colecta es sobre listas de reproducción, videos e información de identificación, como datos de perfil. YSSYNC no puede obtener información de nivel personal de tu cuenta de Google ni de Spotify. ",
    },
    {
        English: "How does YSSYNC work?",
        Japanese: "日本語",
        Spanish: "¿Cómo funciona YSSYNC?",
    },
    {
        English: "YSSYNC retrieves video information from the playlist you select in the application, then, it creates a new playlist in your Spotify account and proceeds to fulfill it with the videos within the previously selected Youtube playlists.",
        Japanese: "日本語",
        Spanish: "YSSYNC colecciona información sobre los videos en las listas de reproducción que seleccionas dentro de la aplicación, después genera una nueva lista en spotify y añade las canciones de las listas previamente seleccionadas.",
    },
    {
        English: "Can I modify my Youtube account from YSSYNC?",
        Japanese: "日本語",
        Spanish: "¿Puedo modificar mi cuenta de Youtube a través de YSSYNC?",
    },
    {
        English: "No. You can not delete, create, or modify Youtube elements in the YSSYNC app. There is no risk of deleting valuable data. However, you can create new Spotify playlists with the application.",
        Japanese: "日本語",
        Spanish: "No, no es posible borrar, crar o modificar elementos de Youtube en la aplicación YSSYNC. No existe riesgo de borrar información importante. Sin embargo, la aplicación permite crear y editar listas de reproducción en Spotify.",
    },
    {
        English: "Can I update a Youtube playlist that I already have in Spotify?",
        Japanese: "日本語",
        Spanish: "¿Puedo actualizar una lista de Youtube que ya tengo en Spotify?",
    },
    {
        English: "Yes, you can. You can add songs to an already synchronized playlist in Youtube, and it will be updated when you synchronize it again. YSSYNC will add the new songs to spotify, but won't delete the ones already there.",
        Japanese: "日本語",
        Spanish: "Sí. Puedes añadir canciones a una lista de Youtube ya sincronizada y se actualizará una vez que la sincronices nuevamente. YSSYNC añadirá las nuevas canciones a Spotify, pero no eliminará las que ya forman parte de la lista.",
    },
    {
        English: "Why is YSSYNC unable to synchronize my Youtube playlist?",
        Japanese: "日本語",
        Spanish: "¿Por qué YSSYNC no puede sincronizar mi lista de reproducción?",
    },
    {
        English: "YSSYNC is unable to synchronize empty playlists. Youtube videos that aren't officially identified as songs by Youtube are ignored by YSSYNC. A playlist made entirely by non-song videos is considered an empty playlist by YSSYNC.",
        Japanese: "日本語",
        Spanish: "YSSYNC no es capaz de sincronizar listas vacías. Los videos de Youtube que no están clasificados oficialmente como canciones por Youtube son ignorados por YSSYNC. Una lista de reproducción hecha solamente de videos que no contienen canciones es considerada una lista vacía por YSSYNC.",
    },
    {
        English: "Contact",
        Japanese: "日本語",
        Spanish: "Contáctanos",
    },
    {
        English: "Loading",
        Japanese: "日本語",
        Spanish: "Cargando",
    },
    {
        English: "IGNORE",
        Japanese: "日本語",
        Spanish: "IGNORAR",
    },
    {
        English: "UNDO",
        Japanese: "日本語",
        Spanish: "DESHACER",
    },
];
