// import type {NextApiRequest, NextApiResponse} from 'next'
// import fs from "fs";
// import fetch from "node-fetch";
// import FormData from 'form-data';
// import {IncomingForm} from 'formidable';
// import {CHAT_FILES_SERVER_HOST} from "@/utils/app/const";

// export const config = {
//     api: {
//         bodyParser: false,
//     }
// };

// const handler = async (req: NextApiRequest, res: NextApiResponse) => {
//     console.log("beginning handler");

//     const fData = await new Promise<{ fields: any, files: any }>((resolve, reject) => {
//         const form = new IncomingForm({
//             multiples: true // 여러 개의 파일 업로드
//         })
//         form.parse(req, (err, fields, files) => {
//             if (err) return reject(err)
//             resolve({ fields, files })
//         })
//     });

//     if (fData?.files) {
//         const files = Object.values(fData.files); // 파일 목록 조회
//         const formData = new FormData();

//         files.forEach((file: {[key:string]: any}) => {
//             formData.append('files', fs.createReadStream(file.filepath), file.originalFilename) // 파일 추가
//         });

//         const response = await fetch(`${CHAT_FILES_SERVER_HOST}/upload/multiple`, { // 경로 변경
//             method: 'POST',
//             body: formData
//         });

//         const result = await response.text();

//         res.status(200).json(result);
//     }
// }

// export default handler;

import type {NextApiRequest, NextApiResponse} from 'next'
import fs from "fs";
import fetch from "node-fetch";
import FormData from 'form-data';
import {IncomingForm} from 'formidable';
import {CHAT_FILES_SERVER_HOST} from "@/utils/app/const";

export const config = {
    api: {
        bodyParser: false,
    }
};

const handler = async (req: NextApiRequest, res: NextApiResponse) => {
    console.log("beginning handler");

    const fData = await new Promise<{ fields: any, files: any }>((resolve, reject) => {
        const form = new IncomingForm({
            multiples: false
        })
        form.parse(req, (err, fields, files) => {
            if (err) return reject(err)
            resolve({ fields, files })
        })
    });

    if (fData?.files.file) {
        const uploadFile = fData.files.file;
        const formData = new FormData();

        formData.append('file', fs.createReadStream(uploadFile.filepath), uploadFile.originalFilename)

        const response = await fetch(`${CHAT_FILES_SERVER_HOST}/upload`, {
            method: 'POST',
            body: formData
        });

        const result = await response.text();

        res.status(200).json(result);
    }
}

export default handler;